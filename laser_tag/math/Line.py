from __future__ import annotations

from .Point import Point


class Line:
    """A line is represented by two points in space"""

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def __repr__(self):
        return f"[{self.point1}, {self.point2}]"

    @staticmethod
    def create(parsed_object) -> Line:
        try:
            point1 = Point.create(parsed_object[0])
            point2 = Point.create(parsed_object[1])
            if point1 is None or point2 is None:
                return None
            return Line(point1, point2)
        except:
            return None
