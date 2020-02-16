from typing import Dict, OrderedDict
import Vehicle
import Intersection
from queue import Queue

class BasicLane(object):
    def __init__(self, ID):
        self.ID = ID
        self.front: Vehicle = None
        self.tail: Vehicle = None
        self.capacity: int = 0
        self.source: Intersection = None
        self.sink: Intersection = None
        # This is used to connect a lane to its sink and source
        self.sinkLanes = Dict[Vehicle.Intention, BasicLane]
        # Add the source lanes in order of priority
        self.sourceLanes = OrderedDict[BasicLane]
        # The incoming cars that were blocked due to limited capacity
        # TODO: This is FIFO, We need PriorityQueue
        self.waitList = Queue(3)

