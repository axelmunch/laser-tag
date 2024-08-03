import pygame

from ....configuration import MAX_PLAYER_NAME_LENGTH, VARIABLES
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....game.Game import Game
from ....language.LanguageKey import LanguageKey
from ....network.ClientServerGroup import ClientServerGroup
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import GraphicalButton
from ..GraphicalText import GraphicalText
from ..GraphicalTextInput import GraphicalTextInput
from .Menu import Menu


class ConnectionMenu(Component, Menu):
    """Connection menu component"""

    def __init__(self, game: Game, callback_main_menu=None):
        Component.__init__(self)
        Menu.__init__(self)

        self.game = game
        self.callback_main_menu = callback_main_menu

        self.client_server = ClientServerGroup()

        self.set_original_size(1920, 1080)

        self.menu_box_width = 1920 - 500
        self.menu_box_height = 1080 - 200
        border_margin = 50
        button_width = (self.menu_box_width - 20 * 5 - border_margin * 2) / 5
        button_height = 100

        self.back_button = GraphicalButton(
            960 - self.menu_box_width / 2 + 50,
            540 + self.menu_box_height / 2 - button_height - 50,
            button_width,
            button_height,
            text_key=LanguageKey.MENU_CONNECTION_BACK,
            action=self.back_action,
        )
        self.join_button_client = GraphicalButton(
            960 - button_width - 50,
            540 + self.menu_box_height / 2 - button_height - 165,
            button_width,
            button_height,
            text_key=LanguageKey.MENU_CONNECTION_JOIN,
            action=lambda: self.client_server.connect_client(
                VARIABLES.latest_join_ip, VARIABLES.latest_join_port, VARIABLES.debug
            ),
        )
        self.host_button_server = GraphicalButton(
            960 + 50,
            540 + self.menu_box_height / 2 - button_height - 165,
            button_width,
            button_height,
        )
        self.join_button_server = GraphicalButton(
            960 + self.menu_box_width / 2 - button_width - 50,
            540 + self.menu_box_height / 2 - button_height - 165,
            button_width,
            button_height,
            text_key=LanguageKey.MENU_CONNECTION_JOIN,
            action=lambda: self.client_server.connect_client(
                "localhost", self.client_server.get_server().get_port(), VARIABLES.debug
            ),
        )
        self.status_text = GraphicalText(
            960 - self.menu_box_width / 2.25 + self.menu_box_width / 2,
            540 - self.menu_box_height / 2 + border_margin + 395,
            align_x="left",
            align_y="center",
            text_key=LanguageKey.MENU_CONNECTION_SERVER_STOPPED,
            size=50,
            color=(0, 0, 255),
        )
        self.hosted_port_text = GraphicalText(
            960 - self.menu_box_width / 2.25 + self.menu_box_width / 2,
            540 - self.menu_box_height / 2 + border_margin + 495,
            align_x="left",
            align_y="center",
            text="",
            size=50,
            color=(0, 0, 255),
        )

        self.elements = [
            self.back_button,
            GraphicalTextInput(
                960 - self.menu_box_width * 7 / 18 / 2,
                540 - self.menu_box_height / 2 + 75,
                self.menu_box_width * 7 / 18,
                button_height,
                default_text=VARIABLES.player_name,
                max_text_length=MAX_PLAYER_NAME_LENGTH,
                unfocus_action=lambda i: self.update_input_value(
                    lambda: setattr(VARIABLES, "player_name", i)
                ),
                no_eval_banned_elements=True,
            ),
            GraphicalText(
                960 - self.menu_box_width / 3,
                540 - self.menu_box_height / 2 + 100,
                align_x="center",
                text_key=LanguageKey.MENU_CONNECTION_JOIN,
                size=50,
                color=(255, 255, 255),
            ),
            GraphicalText(
                960 + self.menu_box_width / 3,
                540 - self.menu_box_height / 2 + 100,
                align_x="center",
                text_key=LanguageKey.MENU_CONNECTION_HOST,
                size=50,
                color=(255, 255, 255),
            ),
            GraphicalText(
                960 - self.menu_box_width / 2.25,
                540 - self.menu_box_height / 2 + border_margin + 200,
                align_x="left",
                align_y="center",
                text_key=LanguageKey.MENU_CONNECTION_IP,
                size=50,
                color=(0, 0, 255),
            ),
            GraphicalTextInput(
                960 - self.menu_box_width / 2.25,
                540 - self.menu_box_height / 2 + border_margin + 225,
                self.menu_box_width * 7 / 18,
                button_height,
                default_text=VARIABLES.latest_join_ip,
                max_text_length=15,
                unfocus_action=lambda i: self.update_input_value(
                    lambda: setattr(VARIABLES, "latest_join_ip", i)
                ),
            ),
            GraphicalText(
                960 - self.menu_box_width / 2.25,
                540 - self.menu_box_height / 2 + border_margin + 400,
                align_x="left",
                align_y="center",
                text_key=LanguageKey.MENU_CONNECTION_PORT,
                size=50,
                color=(0, 0, 255),
            ),
            GraphicalTextInput(
                960 - self.menu_box_width / 2.25,
                540 - self.menu_box_height / 2 + border_margin + 425,
                button_width,
                button_height,
                default_text=VARIABLES.latest_join_port,
                max_text_length=5,
                unfocus_action=lambda i: self.update_input_value(
                    lambda: setattr(VARIABLES, "latest_join_port", i)
                ),
                int_only=True,
                max_int_value=65535,
            ),
            GraphicalText(
                960 - self.menu_box_width / 2.25 + self.menu_box_width / 2,
                540 - self.menu_box_height / 2 + border_margin + 200,
                align_x="left",
                align_y="center",
                text_key=LanguageKey.MENU_CONNECTION_PORT,
                size=50,
                color=(0, 0, 255),
            ),
            GraphicalTextInput(
                960 - self.menu_box_width / 2.25 + self.menu_box_width / 2,
                540 - self.menu_box_height / 2 + border_margin + 225,
                button_width,
                button_height,
                default_text=VARIABLES.latest_host_port,
                max_text_length=5,
                unfocus_action=lambda i: self.update_input_value(
                    lambda: setattr(VARIABLES, "latest_host_port", i)
                ),
                int_only=True,
                max_int_value=65535,
            ),
            self.status_text,
            self.hosted_port_text,
            self.join_button_client,
            self.join_button_server,
            self.host_button_server,
        ]

        self.update()

    def resize(self):
        Menu.resize(self)
        Component.resize(self)

    def update_input_value(self, update_callback):
        if update_callback is not None:
            update_callback()
        VARIABLES.save()

    def back_action(self):
        if self.callback_main_menu is not None:
            self.callback_main_menu()
        self.set_active(False)

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        if self.client_server.is_client_connected():
            self.game.game_paused = False
            self.set_active(False)

        self.join_button_server.set_disabled(not self.client_server.is_server_running())
        if self.client_server.is_server_running():
            # Stop button
            self.host_button_server.set_text_key(LanguageKey.MENU_CONNECTION_STOP)
            self.host_button_server.set_action(lambda: self.client_server.stop_server())
            self.status_text.text_key = LanguageKey.MENU_CONNECTION_SERVER_RUNNING
            self.hosted_port_text.text_str = f"{self.language.get(LanguageKey.MENU_CONNECTION_HOSTED_PORT)} {self.client_server.get_server().get_port()}"
        else:
            # Host button
            self.host_button_server.set_text_key(LanguageKey.MENU_CONNECTION_HOST)
            self.host_button_server.set_action(
                lambda: self.client_server.start_server(
                    VARIABLES.latest_host_port, VARIABLES.debug
                )
            )
            self.status_text.text_key = LanguageKey.MENU_CONNECTION_SERVER_STOPPED
            self.hosted_port_text.text_str = self.language.get(
                LanguageKey.MENU_CONNECTION_HOSTED_PORT
            )

        for event in events:
            if event.id == Event.KEY_ESCAPE_PRESS:
                self.back_action()

        Menu.update(self, events, no_escape=True)
        Component.update(self)

    def render(self):
        self.surface.fill((0, 0, 0))

        pygame.draw.rect(
            self.surface,
            (0, 100, 0),
            (
                resize(960 - self.menu_box_width / 2, "x"),
                resize(540 - self.menu_box_height / 2, "y"),
                resize(self.menu_box_width, "x"),
                resize(self.menu_box_height, "y"),
            ),
        )

        pygame.draw.line(
            self.surface,
            (255, 255, 255),
            (
                resize(960, "x"),
                resize(540 - self.menu_box_height / 2 + 100, "y"),
            ),
            (
                resize(960, "x"),
                resize(540 + self.menu_box_height / 2 - 50, "y"),
            ),
            int(resize(2, "x")),
        )

        menu_title_text = self.text.get_surface(
            self.language.get(LanguageKey.MENU_CONNECTION_TITLE), 50, (255, 255, 255)
        )
        self.surface.blit(
            menu_title_text,
            (
                resize(960, "x") - menu_title_text.get_width() / 2,
                resize(540 - self.menu_box_height / 2 + 20, "y"),
            ),
        )

        for element in self.elements:
            self.surface.blit(
                element.get(), (resize(element.x, "x"), resize(element.y, "y"))
            )

        super().render()
