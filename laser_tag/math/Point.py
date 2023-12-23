from __future__ import annotations


class Point:
    """A point is represented by three positions: x, y and z. If z is not defined, the point is 2D"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"[{self.x},{self.y}]"

    @staticmethod
    def create(parsed_object) -> Point:
        try:
            return Point(float(parsed_object[0]), float(parsed_object[1]))
        except:
            return None
