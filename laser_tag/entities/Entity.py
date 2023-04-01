from ..math.Box import Box
from ..math.Point import Point


class Entity:
    def __init__(self, x, y, z, length, width, height):
        self.position = Point(x, y, z)

        self.collider = Box(
            Point(x - length / 2, y - width / 2, z), length, width, height
        )

        self.rotation = 0
