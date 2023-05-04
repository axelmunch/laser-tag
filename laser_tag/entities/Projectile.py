from __future__ import annotations

from ..math.Point import Point
from .GameEntity import GameEntity


class Projectile(GameEntity):
    """Player entity"""

    def __init__(self, position, parent_id=None):
        super().__init__(position, 0.2, 0.2, 0.2)

        self.move_speed = 0.2
        self.attack_speed = 0
        self.can_be_attacked = False

        self.parent_id = parent_id

    def __repr__(self):
        return f"['{self.__class__.__name__}', {self.position}, {self.rotation}, {self.team}, {self.damages}, {self.score}, {self.eliminations}, {self.parent_id}]"

    @staticmethod
    def create(parsed_object) -> Projectile:
        try:
            position = Point.create(parsed_object[0])
            if position is None:
                return None

            entity = Projectile(position, parsed_object[5])
            entity.rotation = float(parsed_object[1])
            entity.team = int(parsed_object[2])
            entity.damages = int(parsed_object[3])
            entity.score = float(parsed_object[4])
            entity.eliminations = int(parsed_object[5])
            return entity
        except:
            return None

    def death(self):
        # Add eliminations to parent
        pass

        # Add score to parent
        pass
