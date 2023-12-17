from __future__ import annotations

from ..math.Circle import Circle
from ..math.Point import Point


class Entity:
    """Default entity"""

    def __init__(self, position: Point, radius: float):
        self.position = position

        self.collider = Circle(self.position, radius)

        self.rotation = 0

        self.alive = True

    def __repr__(self):
        return f"['{self.__class__.__name__}',{self.position},{self.collider.radius},{self.rotation}]"

    @staticmethod
    def create(parsed_object) -> Entity:
        try:
            position = Point.create(parsed_object[0])
            radius = parsed_object[1]
            if position is None or radius is None:
                return None

            entity = Entity(position, radius)
            entity.rotation = float(parsed_object[2])
            return entity
        except:
            return None

    def move(self, x, y, z):
        self.position.x = x
        self.position.y = y
        self.position.z = z

        self.collider.origin = self.position

    def collides_with(self, other: Entity) -> bool:
        return self.collider.collides_with(other.collider)
