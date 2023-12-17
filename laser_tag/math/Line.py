from __future__ import annotations

from .Point import Point


class Line:
    """A line is represented by two points in space"""

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def get_intersection_line(self, line: Line) -> Point | None:
        """Returns the intersection point between two lines"""
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        x3, y3 = line.point1.x, line.point1.y
        x4, y4 = line.point2.x, line.point2.y

        determinant = (x1 - x2) * (y3 - y4) - (x3 - x4) * (y1 - y2)

        # Parallel lines
        if determinant == 0:
            return None

        # Get intersection point
        x = (
            (x1 * y2 - x2 * y1) * (x3 - x4) - (x1 - x2) * (x3 * y4 - x4 * y3)
        ) / determinant
        y = (
            (x1 * y2 - x2 * y1) * (y3 - y4) - (y1 - y2) * (x3 * y4 - x4 * y3)
        ) / determinant

        return Point(x, y)

    def get_intersection_segment(self, line: Line) -> Point | None:
        """Returns the intersection point between two segments"""
        intersection = self.get_intersection_line(line)
        if intersection is None:
            return None

        if (
            (
                min(line.point1.x, line.point2.x)
                <= intersection.x
                <= max(line.point1.x, line.point2.x)
            )
            and (
                min(line.point1.y, line.point2.y)
                <= intersection.y
                <= max(line.point1.y, line.point2.y)
            )
            and (
                min(self.point1.x, self.point2.x)
                <= intersection.x
                <= max(self.point1.x, self.point2.x)
            )
            and (
                min(self.point1.y, self.point2.y)
                <= intersection.y
                <= max(self.point1.y, self.point2.y)
            )
        ):
            return intersection

        return None

    def __repr__(self):
        return f"[{self.point1},{self.point2}]"

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
