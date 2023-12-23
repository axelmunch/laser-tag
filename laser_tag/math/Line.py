from __future__ import annotations

from math import sqrt

from ..math.distance import distance_points
from .Point import Point


class Line:
    """A line is represented by two points in space"""

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

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

        rounding_precision = 10
        margin = 10**-rounding_precision

        if (
            (
                min(line.point1.x, line.point2.x) - margin
                <= intersection.x
                <= max(line.point1.x, line.point2.x) + margin
            )
            and (
                min(line.point1.y, line.point2.y) - margin
                <= intersection.y
                <= max(line.point1.y, line.point2.y) + margin
            )
            and (
                min(self.point1.x, self.point2.x) - margin
                <= intersection.x
                <= max(self.point1.x, self.point2.x) + margin
            )
            and (
                min(self.point1.y, self.point2.y) - margin
                <= intersection.y
                <= max(self.point1.y, self.point2.y) + margin
            )
        ):
            return intersection

        return None

    def get_coordinates(
        self, map_bounds: tuple[int, int, int, int] = None
    ) -> list[tuple[int, int]]:
        """Returns the coordinates of cells the line passes through

        Parameters:
            map_bounds (int, int, int, int): Map min x, min y, max x, max y
        """

        # DDA: Digital Differential Analyzer
        grid_cells = []

        origin = self.point1

        cell = Point(int(origin.x), int(origin.y))

        max_distance = distance_points(self.point1, self.point2)

        dx = self.point2.x - origin.x
        dy = self.point2.y - origin.y

        one_unit_x = sqrt(1 + (dy / dx) ** 2) if dx != 0 else max_distance
        one_unit_y = sqrt(1 + (dx / dy) ** 2) if dy != 0 else max_distance

        dir_x = 1 if self.point1.x < self.point2.x else -1
        dir_y = 1 if self.point1.y < self.point2.y else -1

        x_distance = (
            ((cell.x + 1 - origin.x) * one_unit_x)
            if dir_x == 1
            else ((origin.x - cell.x) * one_unit_x)
        )
        y_distance = (
            ((cell.y + 1 - origin.y) * one_unit_y)
            if dir_y == 1
            else ((origin.y - cell.y) * one_unit_y)
        )

        grid_cells.append((cell.x, cell.y))

        total_distance = 0
        while total_distance < max_distance:
            if x_distance < y_distance:
                cell.x += dir_x
                total_distance = x_distance
                x_distance += one_unit_x
            else:
                cell.y += dir_y
                total_distance = y_distance
                y_distance += one_unit_y

            if map_bounds is not None:
                if (
                    cell.x < int(map_bounds[0])
                    or cell.x > map_bounds[2]
                    or cell.y < int(map_bounds[1])
                    or cell.y > map_bounds[3]
                ):
                    break

            if total_distance <= max_distance:
                grid_cells.append((cell.x, cell.y))

        return grid_cells
