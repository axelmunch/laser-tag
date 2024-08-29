from math import ceil

import pygame

from ...utils.DeltaTime import DeltaTime
from ..resize import resize
from .Component import Component


class Crosshair(Component):
    """Crosshair component"""

    def __init__(self):
        super().__init__()

        self.set_original_size(50, 50)

        self.space_ratio = 0.5

        self.update()

    def update(self, is_crouching: bool = False):
        """
        Update the component

        Parameters:
            is_crouching (bool): Is the player crouching
        """

        delta_time_value = DeltaTime().get_dt()

        if is_crouching:
            self.space_ratio = max(0, self.space_ratio - delta_time_value * 2)
        else:
            self.space_ratio = min(0.5, self.space_ratio + delta_time_value * 2)

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        color = (192, 192, 192)

        line_width = max(1, int(resize(2, "x")))

        pygame.draw.line(
            self.surface,
            color,
            (self.width / 2, 0),
            (self.width / 2, self.height),
            line_width,
        )

        pygame.draw.line(
            self.surface,
            color,
            (0, self.height / 2),
            (self.width, self.height / 2),
            line_width,
        )

        empty_space_width = ceil(self.width * self.space_ratio)
        empty_space_height = ceil(self.height * self.space_ratio)
        pygame.draw.rect(
            self.surface,
            (0, 0, 0, 0),
            (
                self.width / 2 - (self.width * self.space_ratio) / 2,
                self.height / 2 - (self.height * self.space_ratio) / 2,
                (
                    empty_space_width + 1
                    if empty_space_width % 2 != 0
                    else empty_space_width
                ),
                (
                    empty_space_height + 1
                    if empty_space_height % 2 != 0
                    else empty_space_height
                ),
            ),
        )

        super().render()
