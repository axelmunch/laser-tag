from __future__ import annotations

from time import time

from ..math.Box import Box
from ..math.Point import Point
from .Entity import Entity


class GameEntity(Entity):
    """Entity with game specific properties"""

    def __init__(self, position, length=1, width=1, height=1):
        super().__init__(position, length, width, height)

        self.move_speed = 0.05

        # Attack cooldown (seconds)
        self.attack_speed = 1

        self.next_attack_timestamps = time()

        self.damages = 1

        self.can_move = True
        self.can_attack = True
        self.can_be_attacked = True

        self.score = 0
        self.score_reward = 0
        self.eliminations = 0
        self.team = -1

        self.hp = 0
        self.set_max_hp(1)

    def __repr__(self):
        return f"['{self.__class__.__name__}', {self.position}, {self.collider}, {self.rotation}, {self.team}, {self.score}, {self.eliminations}, {self.hp}, {self.next_attack_timestamps}]"

    @staticmethod
    def create(parsed_object) -> GameEntity:
        try:
            position = Point.create(parsed_object[0])
            collider = Box.create(parsed_object[1])
            if position is None or collider is None:
                return None

            entity = GameEntity(
                position,
                collider.length,
                collider.width,
                collider.height,
            )
            entity.rotation = float(parsed_object[2])
            entity.team = int(parsed_object[3])
            entity.score = float(parsed_object[4])
            entity.eliminations = int(parsed_object[5])
            entity.hp = float(parsed_object[6])
            entity.next_attack_timestamps = float(parsed_object[7])
            return entity
        except:
            return None

    def move(self, x, y, z):
        if self.can_move:
            super().move(x, y, z)

    def set_max_hp(self, max_hp):
        self.max_hp = max_hp
        self.hp = self.max_hp

    def death(self):
        self.alive = False

    def attack(self):
        if self.can_attack and time() >= self.next_attack_timestamps:
            self.next_attack_timestamps = time() + self.attack_speed
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
