from ..configuration import MAX_RAY_DISTANCE
from ..math.Circle import Circle
from ..math.distance import distance_points
from ..math.Line import Line
from ..math.Point import Point
from ..math.rotations import rotate
from .Ray import Ray


class Map:
    """Represents a map in the game and checks collisions"""

    def __init__(self):
        self.map = [
            Line(Point(7.5, 5.5), Point(10, 10)),
            Line(Point(1.5, 0), Point(1.5, 10)),
            Line(Point(0, 1.5), Point(10, 1.5)),
        ]

        # Spatial grid partitioning, stores wall index in each cell
        self.spatial_partitioning = {}
        self.map_min_x = self.map_min_y = self.map_max_x = self.map_max_y = None

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
            line = self.map[i]

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
                self.spatial_partitioning[(x, y)].append(i)

    def collides_with(self, collider: Circle) -> bool:
        for line in self.map:
            if collider.collides_with(line):
                return True

        return False

    def cast_ray(self, origin: Point, direction: float) -> Ray:
        ray = Ray(origin, direction)

        end_point = rotate(MAX_RAY_DISTANCE, direction, center=origin)
        ray_line = Line(origin, end_point)

        intersection_points = []

        for coordinate in ray_line.get_coordinates(map_bounds=self.get_map_bounds()):
            if coordinate not in self.spatial_partitioning:
                continue

            for line_index in self.spatial_partitioning[coordinate]:
                line = self.map[line_index]

                intersection = ray_line.get_intersection_segment(line)
                if intersection is not None:
                    intersection_points.append(intersection)

        if len(intersection_points) > 0:
            intersection_points.sort(
                key=lambda point: distance_points(origin, point),
            )
            # Nearest intersection point
            ray.set_hit(
                intersection_points[0],
                hit_infos=None,
                distance=distance_points(origin, intersection_points[0]),
            )

        return ray
