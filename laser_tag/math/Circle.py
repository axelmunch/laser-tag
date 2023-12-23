from __future__ import annotations

from .distance import distance_points
from .Line import Line
from .Point import Point


class Circle:
    """A circle is represented by an origin point and a radius"""

    def __init__(self, origin: Point, radius: float):
        self.origin = origin
        self.radius = radius

    def __repr__(self):
        return f"[{self.origin},{self.radius}]"

    @staticmethod
    def create(parsed_object) -> Circle:
        try:
            point = Point.create(parsed_object[0])
            radius = float(parsed_object[1])
            if point is None or radius is None:
                return None
            return Circle(point, radius)
        except:
            return None

    def __eq__(self, other) -> bool:
        return self.origin == other.origin and self.radius == other.radius

    def collides_with(self, other: Circle | Line | Point) -> bool:
        if isinstance(other, Circle):
            return self.collides_with_circle(other)
        elif isinstance(other, Line):
            return self.collides_with_segment(other)
        elif isinstance(other, Point):
            return self.collides_with_point(other)
        else:
            raise TypeError(f"Cannot check collision with {type(other)}")

    def collides_with_circle(self, other: Circle) -> bool:
        return distance_points(self.origin, other.origin) <= (
            self.radius + other.radius
        )

    def collides_with_point(self, other: Point) -> bool:
        return distance_points(self.origin, other) <= self.radius

    def collides_with_segment(self, other: Line) -> bool:
        point1_to_center_vector = (
            self.origin.x - other.point1.x,
            self.origin.y - other.point1.y,
        )

        segment_vector = (
            other.point2.x - other.point1.x,
            other.point2.y - other.point1.y,
        )

        # Project the point1 to center vector onto the segment vector
        dot_product = (
            point1_to_center_vector[0] * segment_vector[0]
            + point1_to_center_vector[1] * segment_vector[1]
        )
        segment_length_squared = segment_vector[0] ** 2 + segment_vector[1] ** 2

        if segment_length_squared == 0:
            return distance_points(self.origin, other.point1) <= self.radius

        scale = dot_product / segment_length_squared

        # Nearest point is outside the segment
        if scale < 0:
            nearest_point = other.point1
        elif scale > 1:
            nearest_point = other.point2
        else:
            # Nearest point is on the segment
            nearest_point = Point(
                other.point1.x + scale * segment_vector[0],
                other.point1.y + scale * segment_vector[1],
            )

        return distance_points(self.origin, nearest_point) <= self.radius
