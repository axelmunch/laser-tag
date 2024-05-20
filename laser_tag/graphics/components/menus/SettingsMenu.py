import pygame

from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import GraphicalButton
from .Menu import Menu


class SettingsMenu(Component, Menu):
    """Settings menu component"""

    def __init__(self):
        Component.__init__(self)
        Menu.__init__(self)

        self.set_original_size(1920, 1080)

        self.settings_box_width = 1920 - 500
        self.settings_box_height = 1080 - 200
        button_width = 200
        button_height = 100

        # Create buttons
        self.elements = [
            GraphicalButton(
                960 - self.settings_box_width / 2 + button_height / 2,
                540 + self.settings_box_height / 2 - button_height * 1.5,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_BACK,
                action=lambda: self.set_active(False),
            )
        ]

        self.update()

    def resize(self):
        super().resize()

        try:
            for element in self.elements:
                element.resize()
        except AttributeError:
            pass

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
                resize(960 - self.settings_box_width / 2, "x"),
                resize(540 - self.settings_box_height / 2, "y"),
                resize(self.settings_box_width, "x"),
                resize(self.settings_box_height, "y"),
            ),
        )

        settings_title_text = self.text.get_surface(
            self.language.get(LanguageKey.MENU_SETTINGS_TITLE),
            50,
            (255, 255, 255),
        )
        self.surface.blit(
            settings_title_text,
            (
                resize(960, "x") - settings_title_text.get_width() / 2,
                resize(540 - self.settings_box_height / 2 + 20, "y"),
            ),
        )

        for element in self.elements:
            self.surface.blit(
                element.get(),
                (resize(element.x, "x"), resize(element.y, "y")),
            )

        super().render()
