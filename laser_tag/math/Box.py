from __future__ import annotations

from .Point import Point


class Box:
    """A box is represented by an origin point, a length, a width and a height. If height is not defined, the box is 2D"""

    def __init__(self, origin: Point, length: float, width: float):
        self.origin = origin
        self.length = length
        self.width = width

    def __repr__(self):
        return f"[{self.origin},{self.length},{self.width}]"

    @staticmethod
    def create(parsed_object) -> Box:
        try:
            point = Point.create(parsed_object[0])
            if point is None:
                return None
            return Box(point, float(parsed_object[1]), float(parsed_object[2]))
        except:
            return None

    def collides_with(self, other: Box | Point) -> bool:
        if isinstance(other, Box):
            return self.collides_with_box(other)
        elif isinstance(other, Point):
            return self.collides_with_point(other)
        else:
            raise TypeError(f"Cannot check collision with {type(other)}")

    def collides_with_box(self, other: Box) -> bool:
        return (
            self.origin.x <= other.origin.x + other.length
            and self.origin.x + self.length >= other.origin.x
            and self.origin.y <= other.origin.y + other.width
            and self.origin.y + self.width >= other.origin.y
        )

    def collides_with_point(self, other: Point) -> bool:
        return (
            self.origin.x <= other.x <= self.origin.x + self.length
            and self.origin.y <= other.y <= self.origin.y + self.width
        )
