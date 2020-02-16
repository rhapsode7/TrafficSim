from Lane import BasicLane
from TrafficLight import FourStatesTrafficLight
from Event import *

class FourWayIntersection(object):

    def __init__(self, ID, crossingT = 1):
        self.ID = ID
        self.lanes = []
        self.light = FourStatesTrafficLight(0)
        self.crossingT = crossingT

        # Initialize the intersection to have 9 lanes, numbered counter clockwise started from the left-most lane on the south.
        for i in range(8):
            lane = BasicLane(i)
            lane.sink = self
            self.lanes.append(lane)

    def getLaneStats(self):
        return {i:v for i, v in enumerate(self.lanes)}

    def enterIntersectionFromLaneID(self, T, V, laneID):
        if laneID > len(self.lanes) or laneID < 0:
            return
        Q.put(EnterLane(T, V, self, self.lanes[laneID]))

    def startTrafficLight(self, T):
        Q.put(LightChange(T, self.light))

