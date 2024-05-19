from enum import Enum, auto
from math import ceil

import pygame

from ...events.Event import Event
from ...events.EventInstance import EventInstance
from ...language.LanguageKey import LanguageKey
from ..Button import Button, ButtonState
from ..resize import resize
from .Component import Component


class ButtonType(Enum):
    """Button types"""

    def __str__(self):
        return str(self.value)

    MENU = auto()
    LEVEL_EDITOR = auto()
    LEVEL_EDITOR_ITEM = auto()


class GraphicalButton(Component):
    """Button component"""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        text_key: LanguageKey = None,
        action=None,
        disabled=False,
        selected=False,
        type=ButtonType.MENU,
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.button_width = width
        self.button_height = height
        self.text_key = text_key
        self.action = action
        self.disabled = disabled
        self.selected = selected
        self.type = type

        self.relative_offset_x = 0
        self.relative_offset_y = 0
        self.mouse_x = 0
        self.mouse_y = 0

        self.button = Button(
            self.x,
            self.y,
            self.button_width,
            self.button_height,
            self.text_key,
            self.action,
            self.disabled,
        )

        self.set_original_size(self.button_width, self.button_height)

        self.update()

    def set_disabled(self, disabled: bool):
        self.disabled = disabled
        if disabled:
            self.button.disable()
        else:
            self.button.enable()

    def set_selected(self, selected: bool):
        self.selected = selected

    def set_relative_offset(self, offset_x: float, offset_y: float):
        self.relative_offset_x = offset_x
        self.relative_offset_y = offset_y

    def get_state(self) -> ButtonState:
        return self.button.get_state()

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        self.button.x = self.x
        self.button.y = self.y

        mouse_press = False
        mouse_release = False

        for event in events:
            if event.id == Event.MOUSE_MOVE:
                self.mouse_x = event.data[0] - self.relative_offset_x
                self.mouse_y = event.data[1] - self.relative_offset_y
            elif event.id == Event.MOUSE_LEFT_CLICK_PRESS:
                mouse_press = True
            elif event.id == Event.MOUSE_LEFT_CLICK_RELEASE:
                mouse_release = True

        self.button.update(self.mouse_x, self.mouse_y)

        if mouse_press:
            self.button.click_press()
        elif mouse_release:
            self.button.click_release()

        super().update()

    def render(self):
        button_state = self.button.get_state()

        color = (64, 64, 64)
        if button_state == ButtonState.HOVERED:
            color = (128, 128, 128)
        elif button_state == ButtonState.PRESSED:
            color = (192, 192, 192)

        self.surface.fill(color)

        text_surface = self.text.get_surface(
            self.language.get(self.button.get_text_key()),
            (
                (50 if self.type != ButtonType.LEVEL_EDITOR_ITEM else 25)
                if self.type != ButtonType.LEVEL_EDITOR
                else 30
            ),
            (255, 255, 255),
        )
        self.surface.blit(
            text_surface,
            (
                resize(self.button_width / 2, "x") - text_surface.get_width() / 2,
                resize(self.button_height / 2, "y") - text_surface.get_height() / 2,
            ),
        )

        if self.selected:
            border_size = 6
            pygame.draw.rect(
                self.surface,
                (192, 192, 192),
                (
                    0,
                    0,
                    ceil(resize(self.button_width, "x")),
                    ceil(resize(self.button_height, "y")),
                ),
                max(1, int(resize(border_size, "x"))),
            )

        super().render()
