import pygame

from ...game.Team import Team, get_team_color
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

        self.set_original_size(350, 50 * self.max_length)

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
        pygame.draw.rect(
            self.surface,
            (255, 255, 255, 64),
            (
                0,
                0,
                self.width,
                resize(50 * min(len(self.data), self.max_length), "y"),
            ),
        )

        for i in range(min(len(self.data), self.max_length)):
            data = self.data[i]

            # Team color
            pygame.draw.circle(
                self.surface,
                get_team_color(data[1]),
                (resize(20, "x"), resize(i * 50 + 25, "y")),
                resize(10, "x"),
            )
            if data[1] == Team.NONE:
                pygame.draw.circle(
                    self.surface,
                    (0, 0, 0),
                    (resize(20, "x"), resize(i * 50 + 25, "y")),
                    resize(5, "x"),
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
                    30,
                    (223, 223, 223),
                ),
                (resize(70, "x"), resize(i * 50 + 10, "y")),
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
