from .Point import Point


class Line:
    """A line is represented by two points in space"""

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def __repr__(self):
        return f"[{self.point1}, {self.point2}]"
