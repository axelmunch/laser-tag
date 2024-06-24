import pygame

from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import ButtonType, GraphicalButton
from .Menu import Menu


class SettingsMenu(Component, Menu):
    """Settings menu component"""

    def __init__(self):
        Component.__init__(self)
        Menu.__init__(self)

        self.set_original_size(1920, 1080)

        self.settings_box_width = 1920 - 500
        self.settings_box_height = 1080 - 200
        border_margin = 50
        button_width = (self.settings_box_width - 20 * 5 - border_margin * 2) / 5
        button_height = 100

        self.back_button = GraphicalButton(
            960 - self.settings_box_width / 2 + 50,
            540 + self.settings_box_height / 2 - button_height * 1.5,
            button_width,
            button_height,
            text_key=LanguageKey.MENU_SETTINGS_BACK,
            action=lambda: self.set_active(False),
        )
        self.default_elements = [self.back_button]

        self.pages_buttons = [
            GraphicalButton(
                960
                - self.settings_box_width / 2
                + border_margin
                + 20 * 0
                + button_width * 0,
                540 - self.settings_box_height / 2 + border_margin,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_GENERAL,
                action=lambda: self.switch_settings_page(0),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
            GraphicalButton(
                960
                - self.settings_box_width / 2
                + border_margin
                + 20 * 1
                + button_width * 1,
                540 - self.settings_box_height / 2 + border_margin,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_GRAPHICS,
                action=lambda: self.switch_settings_page(1),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
            GraphicalButton(
                960
                - self.settings_box_width / 2
                + border_margin
                + 20 * 2
                + button_width * 2,
                540 - self.settings_box_height / 2 + border_margin,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_CONTROLS,
                action=lambda: self.switch_settings_page(2),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
            GraphicalButton(
                960
                - self.settings_box_width / 2
                + border_margin
                + 20 * 3
                + button_width * 3,
                540 - self.settings_box_height / 2 + border_margin,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_AUDIO,
                action=lambda: self.switch_settings_page(3),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
            GraphicalButton(
                960
                - self.settings_box_width / 2
                + border_margin
                + 20 * 4
                + button_width * 4,
                540 - self.settings_box_height / 2 + border_margin,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_DEBUG,
                action=lambda: self.switch_settings_page(4),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
        ]
        self.pages_elements = [[], [], [], [], []]
        self.elements = []

        self.switch_settings_page(0)

        self.update()

    def resize(self):
        super().resize()

        try:
            for element in self.elements:
                element.resize()
        except AttributeError:
            pass

    def switch_settings_page(self, page: int):
        # Default
        self.elements = self.default_elements[:]

        for i, element in enumerate(self.pages_buttons):
            element.set_selected(i == page)
            self.elements.append(element)

        for element in self.pages_elements[page]:
            self.elements.append(element)

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
            self.language.get(LanguageKey.MENU_SETTINGS_TITLE), 50, (255, 255, 255)
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
                element.get(), (resize(element.x, "x"), resize(element.y, "y"))
            )

        super().render()
