from __future__ import annotations

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
        return f"['{self.__class__.__name__}', {self.position}, {self.collider}, {self.rotation}]"

    @staticmethod
    def create(parsed_object) -> Entity:
        try:
            position = Point.create(parsed_object[0])
            collider = Box.create(parsed_object[1])
            entity = Entity(
                position.x,
                position.y,
                position.z,
                collider.length,
                collider.width,
                collider.height,
            )
            entity.rotation = float(parsed_object[2])
            return entity
        except:
            return None

    def move(self, x, y, z):
        self.position.x = x
        self.position.y = y
        self.position.z = z

        self.collider.origin.x = x - self.collider.length / 2
        self.collider.origin.y = y - self.collider.width / 2
        self.collider.origin.z = z
