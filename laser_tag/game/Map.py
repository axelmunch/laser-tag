from math import ceil, sqrt

from ..configuration import MAX_RAY_DISTANCE
from ..math.Box import Box
from ..math.Point import Point
from ..math.rotations import rotate
from .Ray import Ray


class Map:
    """Represents a map in the game and checks collisions"""

    def __init__(self):
        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
        # DDA: Digital Differential Analyzer

        ray = Ray(origin, direction)

        cell = Point(int(origin.x), int(origin.y))

        end_point = rotate(1, direction, center=origin)

        dx = end_point.x - origin.x
        dy = end_point.y - origin.y
        one_unit_x = sqrt(1 + (dy / dx) ** 2) if dx != 0 else MAX_RAY_DISTANCE
        one_unit_y = sqrt(1 + (dx / dy) ** 2) if dy != 0 else MAX_RAY_DISTANCE

        x_distance = 0
        y_distance = 0

        casting_direction = [0, 0]
        if direction > 180:
            # Up
            casting_direction[1] = -1
            y_distance = (origin.y - cell.y) * one_unit_y
        else:
            # Down
            casting_direction[1] = 1
            y_distance = (cell.y + 1 - origin.y) * one_unit_y
        if direction > 90 and direction < 270:
            # Left
            casting_direction[0] = -1
            x_distance = (origin.x - cell.x) * one_unit_x
        else:
            # Right
            casting_direction[0] = 1
            x_distance = (cell.x + 1 - origin.x) * one_unit_x

        casting = True
        total_distance = 0
        while casting and total_distance < MAX_RAY_DISTANCE:
            if x_distance < y_distance:
                cell.x += casting_direction[0]
                total_distance = x_distance
                x_distance += one_unit_x
            else:
                cell.y += casting_direction[1]
                total_distance = y_distance
                y_distance += one_unit_y

            # Collision
            if (
                cell.x >= 0
                and cell.x < len(self.map[0])
                and cell.y >= 0
                and cell.y < len(self.map)
            ):
                if self.map[cell.y][cell.x] == 1:
                    casting = False

                    ray.set_hit(
                        rotate(
                            min(total_distance, MAX_RAY_DISTANCE),
                            direction,
                            center=origin,
                        ),
                        hit_infos=None,
                        distance=min(total_distance, MAX_RAY_DISTANCE),
                    )
            else:
                # Out of the map
                casting = False

        return ray
