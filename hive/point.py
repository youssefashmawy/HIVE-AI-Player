class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: "Point") -> 'Point':
        if not isinstance(other, Point):
            print("Error in point.py")
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
