from enum import IntEnum
from Vehicle import Intention


# enum in this class should be defined in order
class TrafficLightState(IntEnum):
    LR = 1
    SR = 2
    RS = 3
    RL = 4

class FourStatesTrafficLight(object):
    def __init__(self, ID, state=TrafficLightState.LR, lengthLR=3, lengthSR=3, lengthRS=3, lengthRL=3):
        self.ID = ID
        self.State = state
        self.AllowedIntention = {
            TrafficLightState.LR: [Intention.LEFT],
            TrafficLightState.SR: [Intention.STRAIGHT, Intention.RIGHT],
            TrafficLightState.RS: [Intention.STRAIGHT, Intention.RIGHT],
            TrafficLightState.RL: [Intention.LEFT],
        }
        self.AllowedLanes = {
            TrafficLightState.LR: [0,1,4,5],
            TrafficLightState.SR: [0,1,4,5],
            TrafficLightState.RS: [2,3,6,7],
            TrafficLightState.RL: [2,3,6,7],
        }
        self.StateLength = {
            TrafficLightState.LR: lengthLR,
            TrafficLightState.SR: lengthSR,
            TrafficLightState.RS: lengthRS,
            TrafficLightState.RL: lengthRL,
        }
        self.nextStateGlobalT = {
            TrafficLightState.LR: 0,
            TrafficLightState.SR: 0,
            TrafficLightState.RS: 0,
            TrafficLightState.RL: 0
        }

    def queryNextState(self):
        return 1 if (self.State + 1) > len(TrafficLightState) else self.State + 1

    def queryPrevState(self):
        return len(TrafficLightState) if self.State - 1 == 0 else self.State - 1