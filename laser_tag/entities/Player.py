from .GameEntity import GameEntity


class Player(GameEntity):
    def __init__(self, x, y, z, length, width, height):
        super().__init__(x, y, z, length, width, height)

        self.move_speed_multiplier = 1

        self.attack_speed = 0.25

        self.set_max_hp(100)
