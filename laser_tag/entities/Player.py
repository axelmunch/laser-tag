from __future__ import annotations

from ..math.Point import Point
from .GameEntity import GameEntity


class Player(GameEntity):
    """Player entity"""

    def __init__(self, position):
        super().__init__(position, 0.5, 0.5, 1)

        self.move_speed = 0.1

        self.attack_speed = 0.25

        self.set_max_hp(100)

    def __repr__(self):
        return f"['{self.__class__.__name__}', {self.position}, {self.rotation}, {self.team}, {self.score}, {self.eliminations}, {self.hp}, {self.next_attack_timestamps}]"

    @staticmethod
    def create(parsed_object) -> Player:
        try:
            position = Point.create(parsed_object[0])
            if position is None:
                return None

            entity = Player(position)
            entity.rotation = float(parsed_object[1])
            entity.team = int(parsed_object[2])
            entity.score = float(parsed_object[3])
            entity.eliminations = int(parsed_object[4])
            entity.hp = float(parsed_object[5])
            entity.next_attack_timestamps = float(parsed_object[6])
            return entity
        except:
            return None
