import pygame

from ...entities.GameEntity import GameEntity
from ...entities.Player import Player
from ...game.Team import get_team_color
from ...language.LanguageKey import LanguageKey
from ..resize import resize
from .Component import Component


class Scoreboard(Component):
    """Scoreboard component"""

    def __init__(
        self,
        data=[],
    ):
        super().__init__()

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
                self.language.get(LanguageKey.GAME_SCOREBOARD_TITLE),
                75,
                (255, 255, 255),
            ),
            (resize(10, "x"), resize(10, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                self.language.get(LanguageKey.GAME_SCOREBOARD_TEAM),
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 0 + 20, "x"), resize(85, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                self.language.get(LanguageKey.GAME_SCOREBOARD_NAME),
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 0.6 + 20, "x"), resize(85, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                self.language.get(LanguageKey.GAME_SCOREBOARD_SCORE),
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 2 + 20, "x"), resize(85, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                self.language.get(LanguageKey.GAME_SCOREBOARD_ELIMINATIONS),
                50,
                (255, 255, 255),
            ),
            (resize(1280 / 5 * 2.75 + 20, "x"), resize(85, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                self.language.get(LanguageKey.GAME_SCOREBOARD_DEATHS),
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
                    get_team_color(entity.team),
                    (resize(20 + 50, "x"), y + resize(step_height / 2, "y")),
                    resize(10),
                )

                # Name
                self.surface.blit(
                    self.text.get_surface(
                        entity.name,
                        40,
                        (255, 255, 255),
                    ),
                    (resize(1280 / 5 * 0.6 + 20, "x"), y),
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
                    (resize(1280 / 5 * 2.75 + 20, "x"), y),
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
