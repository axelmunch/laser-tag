from __future__ import annotations

from time import time

from ..math.Point import Point
from .Entity import Entity


class GameEntity(Entity):
    """Entity with game specific properties"""

    def __init__(self, position: Point, radius: float):
        super().__init__(position, radius)

        self.move_speed = 0.05
        self.run_speed_multiplier = 1.5
        self.crouch_speed_multiplier = 0.5

        # Attack cooldown (seconds)
        self.attack_speed = 1

        self.next_attack_timestamps = time()

        self.damages = 1

        self.can_move = True
        self.can_attack = True
        self.can_be_attacked = True
        self.is_running = False
        self.is_crouching = False

        self.score = 0
        self.score_reward = 0
        self.eliminations = 0
        self.deaths = 0
        self.team = -1

        self.hp = 0
        self.set_max_hp(1)

    def __repr__(self):
        return f"['{self.__class__.__name__}',{self.position},{self.collider.radius},{self.rotation},{self.team},{self.score},{self.eliminations},{self.deaths},{self.hp},{self.next_attack_timestamps},{self.can_move},{self.can_attack}]"

    @staticmethod
    def create(parsed_object) -> GameEntity:
        try:
            position = Point.create(parsed_object[0])
            radius = parsed_object[1]
            if position is None or radius is None:
                return None

            entity = GameEntity(position, radius)
            entity.rotation = float(parsed_object[2])
            entity.team = int(parsed_object[3])
            entity.score = float(parsed_object[4])
            entity.eliminations = int(parsed_object[5])
            entity.deaths = int(parsed_object[6])
            entity.hp = float(parsed_object[7])
            entity.next_attack_timestamps = float(parsed_object[8])
            entity.can_move = bool(parsed_object[9])
            entity.can_attack = bool(parsed_object[10])
            return entity
        except:
            return None

    @staticmethod
    def entity_radius() -> float:
        return 0

    def reset(self):
        self.hp = self.max_hp
        self.next_attack_timestamps = time()
        self.score = 0
        self.eliminations = 0
        self.deaths = 0

    def move(self, x: float, y: float):
        if self.can_move:
            super().move(x, y)

    def set_max_hp(self, max_hp):
        self.max_hp = max_hp
        self.hp = self.max_hp

    def death(self, no_deletion=False):
        if not no_deletion:
            self.alive = False
        self.deaths += 1

    def attack(self) -> bool:
        if (
            self.can_attack
            and time() >= self.next_attack_timestamps
            and not self.is_running
        ):
            self.next_attack_timestamps = time() + self.attack_speed * (
                self.crouch_speed_multiplier if self.is_crouching else 1
            )
            return True
        return False

    def damage(self, damage):
        if self.can_be_attacked:
            self.hp -= damage
            self.hp = max(0, self.hp)
            if self.hp == 0:
                self.death()
                # Killed
                return True
            # Damaged
            return False
        # Can't be attacked
        return None

    def heal(self, heal):
        self.hp += heal
        self.hp = min(self.max_hp, self.hp)

    def on_hit(self, entity: GameEntity):
        pass

    def on_kill(self, entity: GameEntity):
        self.eliminations += 1
        self.score += entity.score_reward
