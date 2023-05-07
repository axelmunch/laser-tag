from math import ceil
from time import time

import pygame

from ...entities.GameEntity import GameEntity
from ...game.Team import get_color
from ...math.rotations import rotate
from ..resize import resize
from ..Text import Text
from .Component import Component


class Leaderboard(Component):
    """Leaderboard component"""

    def __init__(
        self,
        data=[],
    ):
        super().__init__()

        self.text = Text("calibri")

        self.max_length = 5

        self.set_surface_size(250, 50 * self.max_length)

        self.update(data)

    def update(self, leaderboard):
        """
        Update the component.

        Parameters:
            leaderboard (list): Leaderboard (value, team, title)
        """

        self.data = leaderboard
        super().update()

    def render(self):
        self.surface.fill((255, 255, 255, 64))

        for i in range(min(len(self.data), self.max_length)):
            data = self.data[i]

            pygame.draw.circle(
                self.surface,
                get_color(data[1]),
                (resize(20, "x"), resize(i * 50 + 25, "y")),
                resize(10),
            )

            self.surface.blit(
                self.text.get_surface(
                    f"#{i + 1} {data[2]}",
                    30,
                    (255, 255, 255),
                ),
                (resize(40, "x"), resize(i * 50 + 10, "y")),
            )

            value_text = self.text.get_surface(
                data[0],
                30,
                (255, 255, 255),
            )
            self.surface.blit(
                value_text,
                (
                    self.surface.get_width() - resize(10, "x") - value_text.get_width(),
                    resize(i * 50 + 10, "y"),
                ),
            )
