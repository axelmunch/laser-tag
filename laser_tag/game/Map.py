from math import ceil

from ..math.Box import Box
from ..math.Point import Point


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
