import pygame

from ...configuration import DEFAULT_FONT
from ...entities.GameEntity import GameEntity
from ...entities.Player import Player
from ...game.Team import get_color
from ..resize import resize
from ..Text import Text
from .Component import Component


class Scoreboard(Component):
    """Scoreboard component"""

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

        self.set_original_size(1280, 720)

        self.update(data)

    def update(
        self,
        entities: list[GameEntity],
    ):
        """
        Update the component

        Parameters:
            entities (list): List of entities in the world
        """

        self.data = entities
        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 192))

        # Title
        self.surface.blit(
            self.text.get_surface(
                "Scoreboard",
                75,
                (255, 255, 255),
            ),
            (resize(10, "x"), resize(10, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                "Team",
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 0 + 20, "x"), resize(85, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                "Name",
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 1 + 20, "x"), resize(85, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                "Score",
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 2 + 20, "x"), resize(85, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                "Eliminations",
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 3 + 20, "x"), resize(85, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                "Deaths",
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 4 + 20, "x"), resize(85, "y")),
        )

        step_height = 40
        gap = 10
        i = 0
        for entity in self.data:
            if isinstance(entity, Player):
                y = resize(i * (step_height + gap) + 150, "y")

                # Team color
                pygame.draw.circle(
                    self.surface,
                    get_color(entity.team),
                    (resize(20 + 50, "x"), y + resize(step_height / 2, "y")),
                    resize(10),
                )

                # Name
                self.surface.blit(
                    self.text.get_surface(
                        "Name",
                        40,
                        (255, 255, 255),
                    ),
                    (resize(1280 / 5 * 1 + 20, "x"), y),
                )

                # Score
                self.surface.blit(
                    self.text.get_surface(
                        int(entity.score),
                        40,
                        (255, 255, 255),
                    ),
                    (resize(1280 / 5 * 2 + 20, "x"), y),
                )

                # Eliminations
                self.surface.blit(
                    self.text.get_surface(
                        entity.eliminations,
                        40,
                        (255, 255, 255),
                    ),
                    (resize(1280 / 5 * 3 + 20, "x"), y),
                )

                # Deaths
                self.surface.blit(
                    self.text.get_surface(
                        entity.deaths,
                        40,
                        (255, 255, 255),
                    ),
                    (resize(1280 / 5 * 4 + 20, "x"), y),
                )

                i += 1

        super().render()
