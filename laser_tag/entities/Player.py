from __future__ import annotations

from time import time

from ..game.Team import Team
from ..math.Point import Point
from .GameEntity import GameEntity


class Player(GameEntity):
    """Player entity"""

    def __init__(self, position: Point):
        super().__init__(position, Player.entity_radius())

        self.name = ""

        self.move_speed = 0.05

        self.attack_speed = 0.6

        self.damages = 1

        self.score_reward = 100

        self.is_shooting = False
        self.is_moving = False

        self.holding_restart = False

        self.deactivation_time = 4
        self.deactivated_until_timestamp = time()
        self.deactivation_time_ratio = 0

        self.set_max_hp(1)

    def __repr__(self):
        return f"['{self.__class__.__name__}',{self.position},{self.rotation},{self.team},{self.score},{self.eliminations},{self.deaths},{self.hp},{self.next_attack_timestamps},{self.deactivated_until_timestamp},{self.get_deactivation_time_ratio()},{int(self.can_move)},{int(self.can_attack)},{int(self.is_running)},{int(self.is_shooting)},{int(self.is_moving)},{int(self.holding_restart)},'{self.name}']"

    @staticmethod
    def create(parsed_object) -> Player:
        try:
            position = Point.create(parsed_object[0])
            if position is None:
                return None

            entity = Player(position)
            entity.rotation = float(parsed_object[1])
            entity.team = Team(parsed_object[2])
            entity.score = float(parsed_object[3])
            entity.eliminations = int(parsed_object[4])
            entity.deaths = int(parsed_object[5])
            entity.hp = float(parsed_object[6])
            entity.next_attack_timestamps = float(parsed_object[7])
            entity.deactivated_until_timestamp = float(parsed_object[8])
            entity.deactivation_time_ratio = float(parsed_object[9])
            entity.can_move = bool(parsed_object[10])
            entity.can_attack = bool(parsed_object[11])
            entity.is_running = bool(parsed_object[12])
            entity.is_shooting = bool(parsed_object[13])
            entity.is_moving = bool(parsed_object[14])
            entity.holding_restart = bool(parsed_object[15])
            entity.name = str(parsed_object[16])
            return entity
        except:
            return None

    @staticmethod
    def entity_radius() -> float:
        return 0.2

    def get_deactivation_time_ratio(self) -> float:
        return 1 - (self.deactivated_until_timestamp - time()) / self.deactivation_time

    def death(self):
        self.deactivated_until_timestamp = time() + self.deactivation_time
        self.deactivation_time_ratio = 0
        super().death(no_deletion=True)

    def attack(self) -> bool:
        if time() < self.deactivated_until_timestamp:
            return False

        return super().attack()

    def check_can_be_attacked(self) -> bool:
        return (
            time() >= self.deactivated_until_timestamp
            and super().check_can_be_attacked()
        )

    def set_name(self, name: str):
        self.name = name
