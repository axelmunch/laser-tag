from ..math.Box import Box
from ..math.Point import Point
from ..network.safe_eval import safe_eval


class Entity:
    """Default entity"""

    def __init__(self, x, y, z, length, width, height):
        self.position = Point(x, y, z)

        self.collider = Box(
            Point(x - length / 2, y - width / 2, z), length, width, height
        )

        self.rotation = 0

    def __repr__(self):
        return f"[{self.position}, {self.collider}, {self.rotation}]"

    def move(self, x, y, z):
        self.position.x = x
        self.position.y = y
        self.position.z = z

        self.collider.origin.x = x - self.collider.length / 2
        self.collider.origin.y = y - self.collider.width / 2
        self.collider.origin.z = z
