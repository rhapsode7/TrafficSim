
from Vehicle import Intention as intention, BasicVehicle
from Intersection import FourWayIntersection
from Lane import BasicLane
from Event import *



def main():

    # initialize an intersection
    intersection = FourWayIntersection(0)
    vid = 0

    for T in range(1,10,2):
        intersection.enterIntersectionFromLaneID(T, BasicVehicle(vid, intention.LEFT), 0)
        vid += 1
        intersection.enterIntersectionFromLaneID(T, BasicVehicle(vid, intention.STRAIGHT), 1)
        vid += 1
    for T in range(10,20,2):
        intersection.enterIntersectionFromLaneID(T, BasicVehicle(vid, intention.STRAIGHT), 3)
        vid += 1
        intersection.enterIntersectionFromLaneID(T, BasicVehicle(vid, intention.STRAIGHT), 1)
        vid += 1

    intersection.startTrafficLight(0)

    while not Q.empty():
        event = Q.get()
        event.execute()

if __name__ == "__main__":
    main()