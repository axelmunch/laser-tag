import pygame

from ...configuration import DEFAULT_FONT
from ...game.Team import get_color
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

        self.text = Text(
            DEFAULT_FONT["font"],
            DEFAULT_FONT["font_is_file"],
            DEFAULT_FONT["size_multiplier"],
        )

        self.max_length = 5

        self.set_original_size(250, 50 * self.max_length)

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

            # Team color
            pygame.draw.circle(
                self.surface,
                get_color(data[1]),
                (resize(20, "x"), resize(i * 50 + 25, "y")),
                resize(10),
            )

            # Rank and team name
            self.surface.blit(
                self.text.get_surface(
                    f"#{i + 1} {data[2]}",
                    30,
                    (255, 255, 255),
                ),
                (resize(40, "x"), resize(i * 50 + 10, "y")),
            )

            # Score
            value_text = self.text.get_surface(
                data[0],
                30,
                (255, 255, 255),
            )
            self.surface.blit(
                value_text,
                (
                    self.width - resize(10, "x") - value_text.get_width(),
                    resize(i * 50 + 10, "y"),
                ),
            )

        super().render()
