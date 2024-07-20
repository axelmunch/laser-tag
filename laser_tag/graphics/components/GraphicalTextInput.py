from math import ceil

import pygame

from ...events.Event import Event
from ...events.EventInstance import EventInstance
from ...network.safe_eval import eval_banned_elements
from ..Button import Button, ButtonState
from ..resize import resize
from .GraphicalElement import GraphicalElement


class GraphicalTextInput(GraphicalElement):
    """Text input component"""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        default_text: str = "",
        max_text_length: int = 0,
        focus_action=None,
        unfocus_action=None,
        int_only=False,
        no_eval_banned_elements=True,
        disabled=False,
        selected=False,
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.input_width = width
        self.input_height = height
        self.input_value = str(default_text)
        self.max_text_length = max_text_length
        self.focus_action = focus_action
        self.unfocus_action = unfocus_action
        self.int_only = int_only
        self.no_eval_banned_elements = no_eval_banned_elements
        self.disabled = disabled
        self.set_selected(selected)
        self.focused = False

        self.relative_offset_x = 0
        self.relative_offset_y = 0
        self.mouse_x = 0
        self.mouse_y = 0

        self.button = Button(
            self.x,
            self.y,
            self.input_width,
            self.input_height,
            action=self.focus_event,
            disabled=self.disabled,
        )

        self.set_original_size(self.input_width, self.input_height)

        self.update()

    def get_value(self):
        if self.int_only:
            if len(self.input_value) == 0:
                return 0
            return int(self.input_value)
        return self.input_value

    def focus_event(self):
        if self.focus_action is not None:
            self.focus_action()
        self.focused = True

    def unfocus_event(self):
        if self.unfocus_action is not None:
            self.unfocus_action(self.get_value())
        self.focused = False

    def set_disabled(self, disabled: bool):
        self.disabled = disabled
        if disabled:
            self.button.disable()
        else:
            self.button.enable()

    def set_relative_offset(self, offset_x: float, offset_y: float):
        self.relative_offset_x = offset_x
        self.relative_offset_y = offset_y

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
            if self.focused:
                if event.id == Event.TYPE_CHAR:
                    char_to_add = event.data
                    if (
                        len(self.input_value) < self.max_text_length
                        or self.max_text_length == 0
                    ):
                        if self.int_only:
                            if char_to_add in "0123456789":
                                self.input_value += char_to_add
                        else:
                            if self.no_eval_banned_elements:
                                is_safe = True
                                for element in eval_banned_elements:
                                    if element in self.input_value + char_to_add:
                                        is_safe = False
                                if is_safe:
                                    self.input_value += char_to_add
                            else:
                                self.input_value += char_to_add
                if event.id == Event.KEY_BACKSPACE_PRESS:
                    self.input_value = self.input_value[:-1]
                elif event.id == Event.KEY_RETURN_PRESS:
                    self.unfocus_event()

        self.button.update(self.mouse_x, self.mouse_y)

        if mouse_press:
            self.button.click_press()
        elif mouse_release:
            self.button.click_release()
            if self.focused and not self.button.is_hovered():
                self.unfocus_event()

        super().update()

    def render(self):
        button_state = self.button.get_state()

        color = (64, 64, 64)
        if button_state == ButtonState.HOVERED:
            color = (128, 128, 128)
        elif button_state == ButtonState.PRESSED:
            color = (192, 192, 192)

        self.surface.fill(color)

        text_surface = self.text.get_surface(self.input_value, 50, (255, 255, 255))
        self.surface.blit(
            text_surface,
            (
                resize(15, "x"),
                resize(self.input_height / 2, "y") - text_surface.get_height() / 2,
            ),
        )

        if self.disabled:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(64)
            overlay.fill((0, 0, 0))
            self.surface.blit(overlay, (0, 0))

        if self.is_selected() or self.focused:
            border_size = 6
            pygame.draw.rect(
                self.surface,
                (192, 192, 192),
                (
                    0,
                    0,
                    ceil(resize(self.input_width, "x")),
                    ceil(resize(self.input_height, "y")),
                ),
                max(1, int(resize(border_size, "x"))),
            )

        super().render()
