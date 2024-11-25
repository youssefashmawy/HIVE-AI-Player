from .orientation import Orientation
from .point import Point


class Layout:
    """Used to determine the layout of the hexagon there is 2 main layouts pointy-top and flat-top but Hive uses flat-top orientation"""

    # Size represents the scaling factor in the x,y dimensions for the hexagon

    def __init__(
        self,
        orientation: Orientation,
        size: Point,
        origin: Point = Point(0, 0),
    ):
        self.orientation = orientation
        self.size = size
        self.origin = origin
