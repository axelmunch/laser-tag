import pygame

from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import GraphicalButton
from .Menu import Menu


class Disconnected(Component, Menu):
    """Disconnected component"""

    def __init__(
        self,
        callback_menu=None,
    ):
        Component.__init__(self)
        Menu.__init__(self)

        self.set_original_size(1920, 1080)

        self.callback_menu = callback_menu

        self.box_width = 700
        self.box_height = 250
        button_width = 400
        button_height = 100

        # Create buttons
        self.elements = [
            GraphicalButton(
                960 - button_width / 2,
                540 + self.box_height / 2 - button_height - button_height / 5,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_DISCONNECTED_MENU,
                action=lambda: self.menu(),
            )
        ]

        self.update()

    def resize(self):
        Menu.resize(self)
        Component.resize(self)

    def menu(self):
        if self.callback_menu is not None:
            self.callback_menu()
            self.callback_menu = None
        self.set_active(False)

    def deactivate_event(self):
        self.menu()

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        Menu.update(self, events)
        Component.update(self)

    def render(self):
        self.surface.fill((0, 0, 0, 128))

        pygame.draw.rect(
            self.surface,
            (0, 100, 0),
            (
                resize(960 - self.box_width / 2, "x"),
                resize(540 - self.box_height / 2, "y"),
                resize(self.box_width, "x"),
                resize(self.box_height, "y"),
            ),
        )

        disconnected_text = self.text.get_surface(
            self.language.get(LanguageKey.MENU_DISCONNECTED_TITLE),
            50,
            (255, 255, 255),
        )
        self.surface.blit(
            disconnected_text,
            (
                resize(960, "x") - disconnected_text.get_width() / 2,
                resize(540 - self.box_height / 2 + 20, "y"),
            ),
        )

        for element in self.elements:
            self.surface.blit(
                element.get(),
                (resize(element.x, "x"), resize(element.y, "y")),
            )

        super().render()
