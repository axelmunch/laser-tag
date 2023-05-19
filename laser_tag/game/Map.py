from math import ceil

from ..math.Box import Box
from ..math.Point import Point
from ..math.rotations import rotate
from .Ray import Ray


class Map:
    """Represents a map in the game and checks collisions"""

    def __init__(self):
        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def get_spawn_point(self):
        return Point(4, 4)

    def collides_with(self, collider: Box):
        if collider.origin.x < 0 or collider.origin.y < 0:
            return True

        for y in range(
            int(collider.origin.y), ceil(collider.origin.y + collider.width)
        ):
            for x in range(
                int(collider.origin.x), ceil(collider.origin.x + collider.length)
            ):
                if y > len(self.map) - 1 or x > len(self.map[y]) - 1:
                    return True

                if self.map[y][x] == 1:
                    return True

    def cast_ray(self, origin: Point, direction: float) -> Ray:
        max_ray_length = 100

        ray = Ray(origin, direction)

        # Cast
        precision = 5
        for i in range(max_ray_length * precision):
            point = rotate(i / precision, direction, center=origin)
            if self.map[int(point.y)][int(point.x)] == 1:
                ray.set_hit(point, None)
                break

        return ray
