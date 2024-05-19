import pygame

from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import GraphicalButton
from .Menu import Menu


class Confirmation(Component, Menu):
    """Confirmation component"""

    def __init__(
        self,
        text_key: LanguageKey,
        callback_yes=None,
        callback_no=None,
        callback_cancel=None,
    ):
        Component.__init__(self)
        Menu.__init__(self)

        self.set_original_size(1920, 1080)

        self.text_key = text_key
        self.callback_yes = callback_yes
        self.callback_no = callback_no
        self.callback_cancel = callback_cancel

        self.confirmation_box_width = 500
        self.confirmation_box_height = 250
        button_width = 150
        button_height = 150

        # Create buttons
        self.buttons = [
            GraphicalButton(
                960
                - self.confirmation_box_width / 2
                + self.confirmation_box_width / 3
                - button_width / 2,
                540
                + self.confirmation_box_height / 2
                - button_height
                - button_height / 5,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_CONFIRMATION_NO,
                action=lambda: self.no(),
            ),
            GraphicalButton(
                960
                - self.confirmation_box_width / 2
                + self.confirmation_box_width / 3 * 2
                - button_width / 2,
                540
                + self.confirmation_box_height / 2
                - button_height
                - button_height / 5,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_CONFIRMATION_YES,
                action=lambda: self.yes(),
            ),
        ]

        self.update()

    def resize(self):
        super().resize()

        try:
            for button in self.buttons:
                button.resize()
        except AttributeError:
            pass

    def yes(self):
        if self.callback_yes is not None:
            self.callback_yes()
        self.set_active(False)

    def no(self):
        if self.callback_no is not None:
            self.callback_no()
        self.set_active(False)

    def cancel(self):
        if self.callback_cancel is not None:
            self.callback_cancel()

    def deactivate_event(self):
        self.cancel()

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
                resize(960 - self.confirmation_box_width / 2, "x"),
                resize(540 - self.confirmation_box_height / 2, "y"),
                resize(self.confirmation_box_width, "x"),
                resize(self.confirmation_box_height, "y"),
            ),
        )

        confirmation_text = self.text.get_surface(
            self.language.get(self.text_key),
            50,
            (255, 255, 255),
        )
        self.surface.blit(
            confirmation_text,
            (
                resize(960, "x") - confirmation_text.get_width() / 2,
                resize(540 - self.confirmation_box_height / 2 + 20, "y"),
            ),
        )

        for button in self.buttons:
            self.surface.blit(
                button.get(),
                (resize(button.x, "x"), resize(button.y, "y")),
            )

        super().render()
