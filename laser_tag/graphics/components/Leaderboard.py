import pygame

from ...game.Team import Team, get_color
from ..resize import resize
from .Component import Component


class Leaderboard(Component):
    """Leaderboard component"""

    def __init__(
        self,
        data=[],
    ):
        super().__init__()

        self.max_length = 5

        self.set_original_size(275, 50 * self.max_length)

        self.update(data)

    def update(self, leaderboard: list[tuple[float, Team, str]]):
        """
        Update the component

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

            # Rank
            self.surface.blit(
                self.text.get_surface(
                    i + 1,
                    30,
                    (255, 255, 255),
                ),
                (resize(40, "x"), resize(i * 50 + 10, "y")),
            )

            # Name
            self.surface.blit(
                self.text.get_surface(
                    data[2],
                    20,
                    (255, 255, 255),
                ),
                (resize(70, "x"), resize(i * 50 + 17, "y")),
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
