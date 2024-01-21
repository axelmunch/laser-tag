from math import ceil
from typing import TypedDict

from ..configuration import MAX_RAY_DISTANCE
from ..math.Circle import Circle
from ..math.distance import distance_points
from ..math.Line import Line
from ..math.Point import Point
from ..math.rotations import rotate
from .Ray import Ray
from .Wall import Wall


class IntersectionData(TypedDict):
    intersection_point: Point
    line_intersecting: Line
    distance: float


class Map:
    """Represents a map in the game and checks collisions"""

    def __init__(self):
        self.map = [
            Wall(Line(Point(7.5, 5.5), Point(10, 10))),
            Wall(Line(Point(1.5, 0), Point(1.5, 10))),
            Wall(Line(Point(0, 1.5), Point(10, 1.5))),
            Wall(Line(Point(9, 8), Point(9, 11))),
            Wall(Line(Point(3, 12), Point(5, 14))),
            Wall(Line(Point(5, 12), Point(3, 14))),
        ]

        # Spatial grid partitioning, stores wall index in each cell
        self.spatial_partitioning = {}
        self.map_min_x = self.map_min_y = self.map_max_x = self.map_max_y = None

        rounding_precision = 10
        self.margin = 10**-rounding_precision

        self.generate_partitioning_cache()

    def get_spawn_point(self) -> Point:
        return Point(4, 4)

    def get_map_bounds(self) -> tuple[int, int, int, int]:
        return (
            self.map_min_x,
            self.map_min_y,
            self.map_max_x,
            self.map_max_y,
        )

    def generate_partitioning_cache(self):
        self.spatial_partitioning = {}
        self.map_min_x = self.map_min_y = self.map_max_x = self.map_max_y = None

        for i in range(len(self.map)):
            line: Line = self.map[i].get_line()

            # Min and max
            if self.map_min_x is None:
                self.map_min_x = line.point1.x
                self.map_min_y = line.point1.y
                self.map_max_x = line.point1.x
                self.map_max_y = line.point1.y
            self.map_min_x = min(self.map_min_x, line.point1.x, line.point2.x)
            self.map_min_y = min(self.map_min_y, line.point1.y, line.point2.y)
            self.map_max_x = max(self.map_max_x, line.point1.x, line.point2.x)
            self.map_max_y = max(self.map_max_y, line.point1.y, line.point2.y)

            for x, y in line.get_coordinates():
                if (x, y) not in self.spatial_partitioning:
                    self.spatial_partitioning[(x, y)] = []

                if i not in self.spatial_partitioning[(x, y)]:
                    self.spatial_partitioning[(x, y)].append(i)

    def collides_with(self, collider: Circle) -> bool:
        for wall in self.map:
            if collider.collides_with(wall.get_line()):
                return True

        return False

    def cast_ray(self, origin: Point, direction: float) -> Ray:
        ray = Ray(origin, direction)

        end_point = rotate(MAX_RAY_DISTANCE, direction, center=origin)
        ray_line = Line(origin, end_point)

        intersection: IntersectionData = None

        for coordinate in ray_line.get_coordinates(map_bounds=self.get_map_bounds()):
            if coordinate not in self.spatial_partitioning:
                continue

            for wall_index in self.spatial_partitioning[coordinate]:
                line: Line = self.map[wall_index].get_line()

                intersection_point = ray_line.get_intersection_segment(line)
                if intersection_point is not None:
                    # Check intersection point in current cell
                    if (
                        coordinate[0] == int(intersection_point.x - self.margin)
                        or coordinate[0] + 1 == ceil(intersection_point.x + self.margin)
                    ) and (
                        coordinate[1] == int(intersection_point.y - self.margin)
                        or coordinate[1] + 1 == ceil(intersection_point.y + self.margin)
                    ):
                        distance = distance_points(origin, intersection_point)

                        if intersection is None or distance < intersection["distance"]:
                            # Nearest intersection
                            intersection = {
                                "intersection_point": intersection_point,
                                "line_intersecting": line,
                                "distance": distance,
                            }

            if intersection is not None:
                break

        if intersection is not None:
            ray.set_hit(
                intersection["intersection_point"],
                hit_infos=intersection["line_intersecting"].get_point_ratio_on_line(
                    intersection["intersection_point"]
                ),
                distance=intersection["distance"],
            )

        return ray
