from math import ceil

import pygame

from ...events.Event import Event
from ...events.EventInstance import EventInstance
from ..resize import resize
from .GraphicalElement import GraphicalElement


class GraphicalSlider(GraphicalElement):
    """Slider component"""

    def __init__(
        self,
        x: float,
        y: float,
        min_value: float,
        max_value: float,
        default_value: float,
        precision=0,
        change_action=None,
        disabled=False,
        selected=False,
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.min_value = min_value
        self.max_value = max_value
        self.precision = precision
        self.change_action = change_action
        self.current_value = default_value
        self.percentage = (self.current_value - self.min_value) / (
            self.max_value - self.min_value
        )
        self.selecting = False

        self.disabled = disabled
        self.set_selected(selected)

        self.relative_offset_x = 0
        self.relative_offset_y = 0
        self.mouse_x = 0
        self.mouse_y = 0

        self.set_original_size(400, 100)

        self.set_relative_offset(self.x, self.y)

        self.update()

    def set_disabled(self, disabled: bool):
        self.disabled = disabled

    def set_relative_offset(self, offset_x: float, offset_y: float):
        self.relative_offset_x = offset_x
        self.relative_offset_y = offset_y

    def select(self):
        if self.selecting and self.change_action is not None:
            self.change_action(self.current_value)
        self.selecting = False

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

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

        if (
            self.mouse_x >= 0
            and self.mouse_x <= self.original_width
            and self.mouse_y >= 0
            and self.mouse_y <= self.original_height
        ):
            if mouse_press:
                self.selecting = True

        if self.selecting and not self.disabled:
            self.current_value = max(
                self.min_value,
                min(
                    self.max_value,
                    round(
                        self.min_value
                        + (self.max_value - self.min_value)
                        * (self.mouse_x / self.original_width),
                        self.precision,
                    ),
                ),
            )
            self.percentage = (self.current_value - self.min_value) / (
                self.max_value - self.min_value
            )

        if mouse_release:
            if self.selecting:
                self.select()

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        text_color = (255, 255, 255)
        text_size = 50

        text_surface = self.text.get_surface(self.min_value, text_size, text_color)
        text_width_left = text_surface.get_width()
        text_height = text_surface.get_height()
        self.surface.blit(
            text_surface,
            (0, resize(self.original_height, "y") - text_surface.get_height()),
        )
        text_surface = self.text.get_surface(self.max_value, text_size, text_color)
        text_width_right = text_surface.get_width()
        self.surface.blit(
            text_surface,
            (
                resize(self.original_width, "x") - text_surface.get_width(),
                resize(self.original_height, "y") - text_surface.get_height(),
            ),
        )

        text_surface = self.text.get_surface(
            self.current_value if self.precision > 0 else int(self.current_value),
            text_size,
            text_color,
        )
        self.surface.blit(
            text_surface,
            (
                resize(self.original_width / 2, "x") - text_surface.get_width() / 2,
                0,
            ),
        )

        pygame.draw.rect(
            self.surface,
            (128, 128, 128),
            (
                text_width_left,
                resize(self.original_height - 3, "y") - text_height / 2,
                resize(self.original_width, "x") - text_width_left - text_width_right,
                ceil(resize(6, "y")),
            ),
        )
        pygame.draw.rect(
            self.surface,
            (192, 192, 192),
            (
                text_width_left
                + (
                    resize(self.original_width, "x")
                    - text_width_left
                    - text_width_right
                )
                * self.percentage
                - resize(4, "x"),
                resize(self.original_height - 5, "y") - text_height / 2,
                ceil(resize(8, "x")),
                ceil(resize(10, "y")),
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
