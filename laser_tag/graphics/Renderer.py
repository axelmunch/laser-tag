import pygame

from ..configuration import VARIABLES
from ..entities.LaserRay import LaserRay
from ..entities.Player import Player
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..game.Game import Game
from ..network.ClientServerGroup import ClientServerGroup
from . import display
from .components.Crosshair import Crosshair
from .components.Fps import Fps
from .components.GameTimer import GameTimer
from .components.HUD import HUD
from .components.LaserGun import LaserGun
from .components.Leaderboard import Leaderboard
from .components.LevelEditor.LevelEditor import LevelEditor
from .components.menus.ConnectionMenu import ConnectionMenu
from .components.menus.Disconnected import Disconnected
from .components.menus.MainMenu import MainMenu
from .components.menus.Menus import Menus
from .components.menus.ModeTeamSelectionMenu import ModeTeamSelectionMenu
from .components.menus.PauseMenu import PauseMenu
from .components.menus.SettingsMenu import SettingsMenu
from .components.Minimap import Minimap
from .components.NetworkStats import NetworkStats
from .components.Scoreboard import Scoreboard
from .components.World import World
from .resize import resize


class Renderer:
    def __init__(self, clock: pygame.time.Clock):
        self.clock = clock

        self.menus = Menus()
        self.last_game_paused = True
        self.last_level_editor = False
        self.last_client_connected = False
        self.close_game = False
        self.client_server = ClientServerGroup()

        self.init_components()

    def init_components(self):
        self.fps = Fps()
        self.minimap = Minimap()
        self.network_stats = NetworkStats()
        self.leaderboard = Leaderboard()
        self.scoreboard = Scoreboard()
        self.game_timer = GameTimer()
        self.crosshair = Crosshair()
        self.hud = HUD()
        self.laser_gun = LaserGun()
        self.world = World()
        self.components = [
            self.fps,
            self.minimap,
            self.network_stats,
            self.leaderboard,
            self.scoreboard,
            self.game_timer,
            self.crosshair,
            self.hud,
            self.world,
            self.laser_gun,
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

        if VARIABLES.level_editor and not self.last_level_editor:
            self.open_level_editor()
        self.last_level_editor = VARIABLES.level_editor

        if VARIABLES.show_fps:
            self.fps.update(self.clock.get_fps())

        controlled_entity_id = game.world.controlled_entity

        if not VARIABLES.level_editor:

            rays = game.world.cast_rays()
            self.world.update(
                rays,
                game.world.entities.values(),
                game.world.get_entity(game.world.controlled_entity),
            )
            if VARIABLES.show_minimap:
                entity_list = []
                if VARIABLES.show_all_entities_minimap:
                    entity_list = game.world.entities.values()
                else:
                    if controlled_entity_id is not None:
                        entity_list.append(game.world.get_entity(controlled_entity_id))
                self.minimap.update(
                    game.world.map.walls,
                    game.world.map.get_map_bounds(),
                    entity_list,
                    rays=rays,
                )

            self.leaderboard.update(game.game_mode.leaderboard)

            if game.show_scoreboard:
                self.scoreboard.update(game.game_mode.scoreboard)

            self.game_timer.update(
                game.game_mode.grace_period_seconds,
                game.game_mode.grace_period_end,
                game.game_mode.game_time_seconds,
                game.game_mode.game_time_end,
            )

            current_entity = game.world.get_entity(controlled_entity_id)
            if current_entity is not None and isinstance(current_entity, Player):
                self.crosshair.update(
                    current_entity.is_running, current_entity.is_crouching
                )

                self.hud.update(
                    current_entity.deactivation_time_ratio, current_entity.can_attack
                )

                is_moving = False
                for event in events:
                    if event.id == Event.GAME_MOVE:
                        is_moving = True
                        break

                # The player is shooting if there is a laser ray with his id
                is_shooting = False
                for entity in game.world.entities.values():
                    if isinstance(entity, LaserRay):
                        if entity.parent_id == controlled_entity_id:
                            is_shooting = True
                            break

                self.laser_gun.update(
                    is_moving,
                    current_entity.is_running,
                    current_entity.is_crouching,
                    is_shooting,
                )

        self.menus.update(events)

        if game.game_paused and not self.last_game_paused:
            self.menus.open_menu(
                PauseMenu(
                    callback_resume=lambda: setattr(game, "game_paused", False),
                    callback_quit=lambda: self.quit(game),
                )
            )
        self.last_game_paused = game.game_paused

        if not game.game_paused:
            if not game.game_mode.is_game_started():
                game.game_paused = True
                self.last_game_paused = True
                self.menus.open_menu(
                    ModeTeamSelectionMenu(game, callback_quit=lambda: self.quit(game))
                )

            if (
                not self.client_server.is_client_connected()
                and self.last_client_connected
            ):
                game.game_paused = True
                self.last_game_paused = True
                self.client_server.disconnect_client()
                self.menus.open_menu(
                    Disconnected(
                        lambda: self.menus.open_menu(
                            ConnectionMenu(
                                game,
                                callback_main_menu=lambda: self.open_main_menu(game),
                            )
                        )
                    )
                )
            self.last_client_connected = self.client_server.is_client_connected()

    def open_level_editor(self):
        self.menus.open_menu(LevelEditor())

    def quit(self, game: Game):
        game.game_paused = True
        self.client_server.disconnect_client()
        self.open_main_menu(game)

    def open_main_menu(self, game: Game):
        self.menus.open_menu(
            MainMenu(
                lambda: self.menus.open_menu(
                    ConnectionMenu(
                        game, callback_main_menu=lambda: self.open_main_menu(game)
                    )
                ),
                callback_settings=lambda: self.menus.open_menu(SettingsMenu()),
                callback_quit=lambda: setattr(self, "close_game", True),
            )
        )

    def render(self, game: Game):
        # Update display

        if not VARIABLES.level_editor:
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

            # Crosshair
            display.screen.blit(
                self.crosshair.get(),
                (
                    resize(960, "x") - self.crosshair.get().get_width() / 2,
                    resize(540, "y") - self.crosshair.get().get_height() / 2,
                ),
            )

            # HUD
            display.screen.blit(
                self.hud.get(), (0, resize(1080, "y") - self.hud.get().get_height())
            )

            # Laser gun
            laser_gun_offset = self.laser_gun.get_offset()
            display.screen.blit(
                self.laser_gun.get(),
                (
                    resize(960 + laser_gun_offset[0], "x")
                    - self.laser_gun.get().get_width() / 2,
                    resize(1080 + laser_gun_offset[1], "y")
                    - self.laser_gun.get().get_height(),
                ),
            )

        for menu in self.menus.get_menus():
            offset_x = menu.menu_offset_x
            offset_y = menu.menu_offset_y
            display.screen.blit(
                menu.get(), (resize(offset_x, "x"), resize(offset_y, "y"))
            )

        if VARIABLES.show_fps:
            if VARIABLES.level_editor:
                fps_surface = self.fps.get()
                display.screen.blit(
                    fps_surface,
                    (resize(10, "x"), resize(1070, "y") - fps_surface.get_height()),
                )
            else:
                display.screen.blit(self.fps.get(), (resize(10, "x"), resize(10, "y")))
