from __future__ import annotations

from ..math.Point import Point
from .GameEntity import GameEntity


class Player(GameEntity):
    """Player entity"""

    def __init__(self, position: Point):
        super().__init__(position, 0.2)

        self.move_speed = 0.05

        self.attack_speed = 0.25

        self.damages = 1

        self.score_reward = 100

        self.set_max_hp(1)

    def __repr__(self):
        return f"['{self.__class__.__name__}',{self.position},{self.rotation},{self.team},{self.score},{self.eliminations},{self.deaths},{self.hp},{self.next_attack_timestamps},{self.can_move},{self.can_attack}]"

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
            entity.deaths = int(parsed_object[5])
            entity.hp = float(parsed_object[6])
            entity.next_attack_timestamps = float(parsed_object[7])
            entity.can_move = bool(parsed_object[8])
            entity.can_attack = bool(parsed_object[9])
            return entity
        except:
            return None

    def death(self):
        super().death(no_deletion=True)
