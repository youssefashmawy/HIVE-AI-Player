from .orientation import Orientation
from .point import Point


class Layout:
    def __init__(
        self,
        orientation: Orientation,
        size: Point,
        origin: Point = Point(0, 0),
    ):
        self.orientation = orientation
        self.size = size
        self.origin = origin
