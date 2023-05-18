import pygame

from ..configuration import VARIABLES
from ..game.Game import Game
from . import display
from .components.Fps import Fps
from .components.GameTimer import GameTimer
from .components.Leaderboard import Leaderboard
from .components.Minimap import Minimap
from .components.NetworkStats import NetworkStats
from .components.Scoreboard import Scoreboard
from .resize import resize


class Renderer:
    def __init__(self, clock: pygame.time.Clock):
        self.clock = clock
        # Load resources

        self.fps = Fps()
        self.minimap = Minimap()
        self.network_stats = NetworkStats()
        self.leaderboard = Leaderboard()
        self.scoreboard = Scoreboard()
        self.game_timer = GameTimer()
        self.components = [
            self.fps,
            self.minimap,
            self.network_stats,
            self.leaderboard,
            self.scoreboard,
            self.game_timer,
        ]

    def set_network_stats(
        self,
        pings: list[float],
        connected: bool,
        bytes_sent: list[int],
        bytes_received: list[int],
    ):
        if VARIABLES.show_network_stats:
            self.network_stats.update(pings, connected, bytes_sent, bytes_received)

    def resize(self):
        for component in self.components:
            component.resize()

    def render(self, game: Game):
        # Update display
        display.screen.fill((42, 42, 42))

        self.minimap.update(game.world.map.map, game.world.entities.values())
        display.screen.blit(self.minimap.get(), (resize(10, "x"), resize(10, "y")))

        self.leaderboard.update(game.game_mode.leaderboard)
        display.screen.blit(
            self.leaderboard.get(),
            (
                resize(1080, "x"),
                resize(10, "y"),
            ),
        )

        network_stats_width = 0
        if VARIABLES.show_network_stats:
            network_stats_surface = self.network_stats.get()
            network_stats_width = network_stats_surface.get_width()
            display.screen.blit(
                network_stats_surface,
                (
                    resize(1910, "x") - network_stats_surface.get_width(),
                    resize(10, "y"),
                ),
            )

        if game.show_scoreboard:
            self.scoreboard.update(list(game.world.entities.values()))
            scoreboard = self.scoreboard.get()
            display.screen.blit(
                scoreboard,
                (
                    resize(960, "x") - scoreboard.get_width() / 2,
                    resize(540, "y") - scoreboard.get_height() / 2,
                ),
            )

        self.game_timer.update(
            game.game_mode.grace_period_seconds,
            game.game_mode.grace_period_end,
            game.game_mode.game_time_seconds,
            game.game_mode.game_time_end,
        )
        game_timer = self.game_timer.get()
        display.screen.blit(
            game_timer,
            (
                resize(1910, "x")
                - game_timer.get_width()
                - (
                    network_stats_width + resize(10, "x")
                    if network_stats_width > 0
                    else 0
                ),
                resize(10, "y"),
            ),
        )

        if VARIABLES.show_fps:
            self.fps.update(self.clock.get_fps())
            display.screen.blit(self.fps.get(), (resize(10, "x"), resize(10, "y")))
