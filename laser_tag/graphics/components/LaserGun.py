from math import sin

from ...utils.DeltaTime import DeltaTime
from ..AssetsLoader import TextureNames
from ..resize import resize
from ..Textures import Textures
from .Component import Component

textures = Textures()


class LaserGun(Component):
    """Laser gun component"""

    def __init__(self):
        super().__init__()

        self.offset_x = 0
        self.offset_y = 0
        self.total_time = 0
        self.multiplier = 0
        self.is_shooting = False

        self.set_original_size(500, 250)

        self.update()

    def get_offset(self) -> tuple[int, int]:
        return self.offset_x, self.offset_y

    def update(
        self,
        is_moving: bool = True,
        is_running: bool = False,
        is_crouching: bool = False,
        is_shooting: bool = False,
    ):
        """
        Update the component

        Parameters:
            is_moving (bool): Is the player moving
            is_running (bool): Is the player running
            is_crouching (bool): Is the player crouching
            is_shooting (bool): Is the player shooting
        """

        self.is_shooting = is_shooting

        delta_time_value = DeltaTime().get_dt()

        if is_crouching:
            self.multiplier = 0
        elif is_running:
            self.multiplier = min(1.75, self.multiplier + delta_time_value * 2)
        elif is_moving:
            # Progressively set to 1 (from 0 or 2)
            if self.multiplier > 1:
                self.multiplier = max(1, self.multiplier - delta_time_value * 3)
            elif self.multiplier < 1:
                self.multiplier = min(1, self.multiplier + delta_time_value * 3)
        else:
            # Progressively set to 0.25 (from 0 or 2)
            if self.multiplier > 0.25:
                self.multiplier = max(0.25, self.multiplier - delta_time_value * 1)
            elif self.multiplier < 0.25:
                self.multiplier = min(0.25, self.multiplier + delta_time_value * 1)

        if self.multiplier > 0:
            self.total_time += delta_time_value * 5 * self.multiplier
            self.offset_x = (
                sin(self.total_time)
                * 20
                * (min(self.multiplier * 2, 1) if not is_moving else 1)
            )
            self.offset_y = (
                abs(sin(self.total_time))
                * 50
                * (min(self.multiplier * 2, 1) if not is_moving else 1)
            )
        else:
            sign_offset_x = 1 if self.offset_x > 0 else -1
            sign_offset_y = 1 if self.offset_y > 0 else -1

            self.offset_x = (
                max(0, abs(self.offset_x) - delta_time_value * 40) * sign_offset_x
            )
            self.offset_y = (
                max(0, abs(self.offset_y) - delta_time_value * 100) * sign_offset_y
            )

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        texture_name = TextureNames.GREEN if not self.is_shooting else TextureNames.RED
        texture = textures.resize_texture(
            texture_name,
            (self.original_width, self.original_height),
        )
        self.surface.blit(
            texture,
            (
                resize(self.original_width / 2, "x") - texture.get_width() / 2,
                resize(self.original_height, "y") - texture.get_height(),
            ),
        )

        super().render()
