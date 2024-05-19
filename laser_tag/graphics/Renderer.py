import pygame

from ..configuration import VARIABLES
from ..events.EventInstance import EventInstance
from ..game.Game import Game
from . import display
from .components.Fps import Fps
from .components.GameTimer import GameTimer
from .components.Leaderboard import Leaderboard
from .components.LevelEditor.LevelEditor import LevelEditor
from .components.menus.Menus import Menus
from .components.menus.PauseMenu import PauseMenu
from .components.Minimap import Minimap
from .components.NetworkStats import NetworkStats
from .components.Scoreboard import Scoreboard
from .components.World import World
from .resize import resize


class Renderer:
    def __init__(self, clock: pygame.time.Clock):
        self.clock = clock

        self.menus = Menus()
        self.last_game_paused = False
        self.close_game = False

        self.init_components()

    def init_components(self):
        self.fps = Fps()
        self.minimap = Minimap()
        self.network_stats = NetworkStats()
        self.leaderboard = Leaderboard()
        self.scoreboard = Scoreboard()
        self.game_timer = GameTimer()
        self.world = World()
        self.level_editor = LevelEditor()
        self.pause_menu = PauseMenu()
        self.components = [
            self.fps,
            self.minimap,
            self.network_stats,
            self.leaderboard,
            self.scoreboard,
            self.game_timer,
            self.world,
            self.level_editor,
        ]

    def set_network_stats(
        self,
        pings: list[float],
        connected: bool,
        bytes_sent: list[int],
        bytes_received: list[int],
    ):
        self.network_stats.update(pings, connected, bytes_sent, bytes_received)

    def close_game_event(self) -> bool:
        return self.close_game

    def resize(self):
        for component in self.components:
            component.resize()
        self.menus.resize()

    def update(self, game: Game, events: list[EventInstance]):
        # Update components

        if VARIABLES.show_fps:
            self.fps.update(self.clock.get_fps())

        if VARIABLES.level_editor:
            self.level_editor.update(events)
            return

        rays = game.world.cast_rays()
        self.world.update(
            rays,
            game.world.entities.values(),
            game.world.get_entity(game.world.controlled_entity),
        )
        self.minimap.update(
            game.world.map.walls,
            game.world.map.get_map_bounds(),
            game.world.entities.values(),
            rays=rays,
        )

        self.leaderboard.update(game.game_mode.leaderboard)

        if game.show_scoreboard:
            self.scoreboard.update(list(game.world.entities.values()))

        self.game_timer.update(
            game.game_mode.grace_period_seconds,
            game.game_mode.grace_period_end,
            game.game_mode.game_time_seconds,
            game.game_mode.game_time_end,
        )

        self.menus.update(events)

        if game.game_paused and game.game_paused != self.last_game_paused:
            self.pause_menu = PauseMenu()
            self.menus.open_menu(self.pause_menu)
        self.last_game_paused = game.game_paused

        if game.game_paused:
            pause_menu_status = self.pause_menu.get_status()
            if pause_menu_status[0]:
                game.game_paused = False
            if pause_menu_status[1]:
                self.close_game = True

    def render(self, game: Game):
        # Update display

        if VARIABLES.level_editor:
            display.screen.blit(self.level_editor.get(), (0, 0))

            if VARIABLES.show_fps:
                fps_surface = self.fps.get()
                display.screen.blit(
                    fps_surface,
                    (resize(10, "x"), resize(1070, "y") - fps_surface.get_height()),
                )
            return

        display.screen.blit(self.world.get(), (0, 0))

        display.screen.blit(self.minimap.get(), (resize(10, "x"), resize(10, "y")))

        display.screen.blit(
            self.leaderboard.get(),
            (
                resize(20 + self.minimap.get_size()[0], "x"),
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
            scoreboard = self.scoreboard.get()
            display.screen.blit(
                scoreboard,
                (
                    resize(960, "x") - scoreboard.get_width() / 2,
                    resize(540, "y") - scoreboard.get_height() / 2,
                ),
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

        for menu in self.menus.get_menus():
            offset_x = menu.menu_offset_x
            offset_y = menu.menu_offset_y
            display.screen.blit(
                menu.get(), (resize(offset_x, "x"), resize(offset_y, "y"))
            )

        if VARIABLES.show_fps:
            display.screen.blit(self.fps.get(), (resize(10, "x"), resize(10, "y")))
