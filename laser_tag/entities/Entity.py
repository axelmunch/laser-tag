from __future__ import annotations

from ..math.Box import Box
from ..math.Point import Point
from ..network.safe_eval import safe_eval


class Entity:
    """Default entity"""

    def __init__(self, position, length, width, height):
        self.position = position

        self.collider = Box(
            Point(position.x - length / 2, position.y - width / 2, position.z),
            length,
            width,
            height,
        )

        self.rotation = 0

        self.alive = True

    def __repr__(self):
        return f"['{self.__class__.__name__}',{self.position},{self.collider},{self.rotation}]"

    @staticmethod
    def create(parsed_object) -> Entity:
        try:
            position = Point.create(parsed_object[0])
            collider = Box.create(parsed_object[1])
            if position is None or collider is None:
                return None

            entity = Entity(
                position,
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

    def collides_with(self, other: Entity) -> bool:
        return self.collider.collides_with(other.collider)
