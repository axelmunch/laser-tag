from __future__ import annotations

from time import time

from .Entity import Entity


class GameEntity(Entity):
    def __init__(self, x, y, z, length=1, width=1, height=1):
        super().__init__(x, y, z, length, width, height)

        self.move_speed_multiplier = 1

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

    def move(self, x, y, z):
        if self.can_move:
            super().move(x, y, z)

    def set_max_hp(self, max_hp):
        self.max_hp = max_hp
        self.hp = self.max_hp

    def death(self):
        pass

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
                return True
            return False
        return None

    def heal(self, heal):
        self.hp += heal
        self.hp = min(self.max_hp, self.hp)

    def on_hit(self, entity: GameEntity):
        pass

    def on_kill(self, entity: GameEntity):
        self.eliminations += 1
        self.score += entity.score_reward
