from __future__ import annotations

from ..math.Point import Point
from .GameEntity import GameEntity


class BarrelTall(GameEntity):
    """Tall barrel entity"""

    def __init__(self, position: Point):
        super().__init__(position, BarrelTall.entity_radius())

        self.can_move = False
        self.can_attack = False
        self.can_be_attacked = False

        self.set_max_hp(1)

    def __repr__(self):
        return f"['{self.__class__.__name__}',{self.position}]"

    @staticmethod
    def create(parsed_object) -> BarrelTall:
        try:
            position = Point.create(parsed_object[0])
            if position is None:
                return None

            return BarrelTall(position)
        except:
            return None

    @staticmethod
    def entity_radius() -> float:
        return 0.2

    def death(self):
        super().death(no_deletion=True)
