from math import ceil

import pygame

from ...events.Event import Event
from ...events.EventInstance import EventInstance
from ..Button import Button, ButtonState
from ..resize import resize
from .GraphicalElement import GraphicalElement


class GraphicalCheckbox(GraphicalElement):
    """Checkbox component"""

    def __init__(
        self,
        x: float,
        y: float,
        default_checked: bool,
        check_action=None,
        uncheck_action=None,
        disabled=False,
        selected=False,
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.checkbox_width = 50
        self.checkbox_height = 50
        self.checked = default_checked
        self.check_action = check_action
        self.uncheck_action = uncheck_action
        self.disabled = disabled
        self.set_selected(selected)

        self.relative_offset_x = 0
        self.relative_offset_y = 0
        self.mouse_x = 0
        self.mouse_y = 0

        self.button = Button(
            self.x,
            self.y,
            self.checkbox_width,
            self.checkbox_height,
            disabled=self.disabled,
        )

        self.set_original_size(self.checkbox_width, self.checkbox_height)

        self.update()

    def set_disabled(self, disabled: bool):
        self.disabled = disabled
        if disabled:
            self.button.disable()
        else:
            self.button.enable()

    def set_relative_offset(self, offset_x: float, offset_y: float):
        self.relative_offset_x = offset_x
        self.relative_offset_y = offset_y

    def toggle(self):
        self.checked = not self.checked

        if self.checked:
            if self.check_action is not None:
                self.check_action()
        else:
            if self.uncheck_action is not None:
                self.uncheck_action()

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

        if self.button.get_state() == ButtonState.RELEASED:
            self.toggle()

        super().update()

    def render(self):
        button_state = self.button.get_state()

        color = (64, 64, 64)
        if button_state == ButtonState.HOVERED:
            color = (128, 128, 128)
        elif button_state == ButtonState.PRESSED:
            color = (192, 192, 192)

        self.surface.fill(color)

        if self.checked:
            text_surface = self.text.get_surface(
                "X",
                25,
                (255, 255, 255),
            )
            self.surface.blit(
                text_surface,
                (
                    resize(self.checkbox_width / 2, "x") - text_surface.get_width() / 2,
                    resize(self.checkbox_height / 2, "y")
                    - text_surface.get_height() / 2,
                ),
            )

        if self.is_selected():
            border_size = 6
            pygame.draw.rect(
                self.surface,
                (192, 192, 192),
                (
                    0,
                    0,
                    ceil(resize(self.checkbox_width, "x")),
                    ceil(resize(self.checkbox_height, "y")),
                ),
                max(1, int(resize(border_size, "x"))),
            )

        super().render()
