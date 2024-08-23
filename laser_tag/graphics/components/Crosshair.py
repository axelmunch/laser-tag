from math import ceil

import pygame

from ..resize import resize
from .Component import Component


class Crosshair(Component):
    """Crosshair component"""

    def __init__(self):
        super().__init__()

        self.set_original_size(50, 50)

        self.update()

    def update(self):
        """
        Update the component
        """

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        color = (192, 192, 192)

        line_width = max(1, int(resize(3, "x")))

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

        pygame.draw.rect(
            self.surface,
            (0, 0, 0, 0),
            (
                self.width / 4,
                self.height / 4,
                ceil(self.width / 2),
                ceil(self.height / 2),
            ),
        )

        super().render()
