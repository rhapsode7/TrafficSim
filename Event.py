import Vehicle
import Lane
import TrafficLight
from TrafficLight import TrafficLightState
from Vehicle import Intention
import Intersection
import queue

DELAY = 1
MAX_T = 50


# initialize Event Queue
Q = queue.PriorityQueue()


class Event(object):
    def __init__(self, T: int, vehicle, light, lane):
        self.T = 0  # Global Time
        self.V = None  # Vehicle ID

    def execute(self):
        pass

    def dispatch(self, event):
        # Put another event into the event queue
        Q.put(event)

    def chain(self, event):
        # This method is used to run another event without putting it to the event queue, very bad design.
        event.execute()

    def __lt__(self, other):
        return self.T < other.T

    def __gt__(self, other):
        return self.T > other.T

    def __le__(self, other):
        return self.T <= other.T


class ArriveCrossing(Event):
    def __init__(self, T: int, V: Vehicle, C: Intersection, L: Lane):
        self.T = T
        self.V = V
        self.L = L
        self.C = C

    def execute(self):
        light = self.C.light

        #update the lane front pointer
        self.L.front = self.V

        print("%d:::Car %d Arrived the Intersection %d from lane %d, Light is %s, Intention is %s" %
              (self.T, self.V.ID, self.C.ID, self.L.ID, TrafficLightState(light.State).name, Intention(self.V.intention).name))

        # If the the lane the vehicle is travelling to is full, add this vehicle to waitlist of the target lane
        if self.L.sinkLanes[self.V.intention].capacity == 0:
            self.L.sinkLanes[self.V.intention].waitlist.put_nowait(self.V)

        # if the vehicle can immediately pass the crossing, send a exit event
        elif self.V.intention in light.AllowedIntention[light.State] and self.L.ID in light.AllowedLanes[light.State]:
            self.chain(ExitCrossing(self.T, self.V, self.C, self.L))
        # Otherwise find out the exit time (waitTime, wT)
        else:
            wt = min([T for LS, T in light.nextStateGlobalT.items() if
                      self.V.intention in light.AllowedIntention[LS] and self.L.ID in light.AllowedLanes[LS]]) - self.T
            self.dispatch(ExitCrossing(self.T + wt, self.V, self.C, self.L))



class ExitCrossing(Event):
    def __init__(self,  T: int, V: Vehicle,  C: Intersection, L: Lane):
        self.T = T
        self.V = V
        self.C = C
        self.L = L

    def execute(self):

        light = self.C.light

        # Set lane front pointer to Null and decrease the counter
        self.L.front = None
        self.L.capacity -= 1
        # TODO: ADD THIS VEHICLE TO ANOTHER LANE

        # if there is no more vehicle in this lane, update the tail pointer
        if self.L.capacity == 0:
            self.L.tail = None
        # otherwise, make the follower arriving the crossing, after a small delay
        else:
            self.dispatch(ArriveCrossing( self.T + DELAY, self.V.follower, self.C, self.L))

        print("%d:::Car %d Left the Intersection %d from Lane %d, Light is %s, Intention is %s" %
              (self.T, self.V.ID, self.C.ID, self.L.ID, TrafficLightState(light.State).name, Intention(self.V.intention).name))


class EnterLane(Event):
    def __init__(self, T: int, V: Vehicle, C : Intersection, L: Lane):
        self.T = T
        self.V = V
        self.L = L
        self.C = C

    def execute(self):
        # if the lane is empty, immediately make it arrival at the crossing, after a small delay?
        if self.L.capacity == 0:
            self.dispatch(ArriveCrossing( self.T + DELAY, self.V, self.C, self.L))
        # otherwise update its tail
        else:
            self.L.tail.follower = self.V
        self.L.tail = self.V
        self.L.capacity += 1
        print("%d:::Car %d Entered Lane %d" % (self.T, self.V.ID, self.L.ID))


class LightChange(Event):

    def __init__(self, T: int, light: TrafficLight):
        self.Light = light
        self.T = T

    def execute(self):
        currentState = self.Light.State
        nextState = self.Light.queryNextState()
        prevState = self.Light.queryPrevState()
        elapsedT = self.Light.StateLength[currentState]

        print("%d:::Light %d Changed from %s to %s" % (self.T, self.Light.ID,
                                                       TrafficLightState(currentState).name, TrafficLightState(nextState).name))
        self.Light.State = nextState

        # Schedule for next LightChange event
        nextState = self.Light.queryNextState()
        for k, v in self.Light.nextStateGlobalT.items():
            self.Light.nextStateGlobalT[k] += elapsedT
        if self.Light.nextStateGlobalT[nextState] < MAX_T:
            self.dispatch(LightChange(self.Light.nextStateGlobalT[nextState], self.Light))


class NotifyWaitlist(Event):
    def __init__(self, T: int, C : Intersection, L: Lane):
        self.T = T
        self.L = L
        self.C = C

    def execute(self):

        # Avoid This
        # for V in self.L.waitlist
        #   self.chain(ArriveCrossing(self.T, V, self.C, self.L))
        # Cause deadloop

        buf = []
        while not self.L.waitlist.empty():
            buf.append(self.L.waitlist.get_nowait())
        for V in buf:
            self.chain(ArriveCrossing(self.T, V, self.C, self.L))