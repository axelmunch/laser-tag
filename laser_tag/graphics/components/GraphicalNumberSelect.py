from math import ceil

import pygame

from ...events.EventInstance import EventInstance
from ..resize import resize
from .GraphicalButton import ButtonType, GraphicalButton
from .GraphicalElement import GraphicalElement


class GraphicalNumberSelect(GraphicalElement):
    """Number select component"""

    def __init__(
        self,
        x: float,
        y: float,
        min_value: float,
        max_value: float,
        default_value: float,
        step=1,
        change_action=None,
        disabled=False,
        selected=False,
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.change_action = change_action
        self.current_value = default_value

        self.set_selected(selected)

        button_size = 50

        self.set_original_size(200, 100)

        self.decrease_button = GraphicalButton(
            0,
            self.original_height / 2 - button_size / 2,
            button_size,
            button_size,
            text="-",
            action=self.decrease,
            selected=False,
            type=ButtonType.MINI_BUTTON,
        )
        self.increase_button = GraphicalButton(
            self.original_width - button_size,
            self.original_height / 2 - button_size / 2,
            button_size,
            button_size,
            text="+",
            action=self.increase,
            selected=False,
            type=ButtonType.MINI_BUTTON,
        )

        self.set_disabled(disabled)
        self.set_relative_offset(self.x, self.y)

        self.change(self.current_value)

        self.update()

    def resize(self):
        super().resize()

        try:
            self.decrease_button.resize()
            self.increase_button.resize()
        except AttributeError:
            pass

    def set_disabled(self, disabled: bool):
        self.decrease_button.set_disabled(disabled)
        self.increase_button.set_disabled(disabled)

    def set_relative_offset(self, offset_x: float, offset_y: float):
        self.decrease_button.set_relative_offset(offset_x, offset_y)
        self.increase_button.set_relative_offset(offset_x, offset_y)

    def decrease(self):
        self.change(self.current_value - self.step)

    def increase(self):
        self.change(self.current_value + self.step)

    def change(self, value: float):
        old_value = self.current_value
        self.current_value = min(self.max_value, max(self.min_value, value))
        if self.current_value == self.min_value:
            self.decrease_button.set_disabled(True)
        else:
            self.decrease_button.set_disabled(False)
        if self.current_value == self.max_value:
            self.increase_button.set_disabled(True)
        else:
            self.increase_button.set_disabled(False)

        if old_value != self.current_value and self.change_action is not None:
            self.change_action(self.current_value)

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        self.decrease_button.update(events)
        self.increase_button.update(events)

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        text_color = (255, 255, 255)
        text_size = 50

        text_surface = self.text.get_surface(
            (
                int(self.current_value)
                if self.current_value == int(self.current_value)
                else self.current_value
            ),
            text_size,
            text_color,
        )
        self.surface.blit(
            text_surface,
            (
                resize(self.original_width / 2, "x") - text_surface.get_width() / 2,
                resize(self.original_height / 2, "y") - text_surface.get_height() / 2,
            ),
        )

        decrease_button_surface = self.decrease_button.get()
        self.surface.blit(
            decrease_button_surface,
            (
                resize(0, "x"),
                resize(self.original_height / 2, "y")
                - decrease_button_surface.get_height() / 2,
            ),
        )
        increase_button_surface = self.increase_button.get()
        self.surface.blit(
            increase_button_surface,
            (
                resize(self.original_width, "x") - increase_button_surface.get_width(),
                resize(self.original_height / 2, "y")
                - increase_button_surface.get_height() / 2,
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
                    ceil(resize(self.original_width, "x")),
                    ceil(resize(self.original_height, "y")),
                ),
                max(1, int(resize(border_size, "x"))),
            )

        super().render()
