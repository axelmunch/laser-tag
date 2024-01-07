from math import ceil

import pygame

from ....configuration import DEFAULT_FONT
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....math.Point import Point
from ...resize import resize
from ...Text import Text
from ..Button import Button, ButtonState
from ..Component import Component
from .Item import Item


class ItemMenu(Component):
    """Level editor item menu component"""

    def __init__(
        self,
        data=[],
    ):
        super().__init__()

        self.text = Text(
            DEFAULT_FONT["font"],
            DEFAULT_FONT["font_is_file"],
            DEFAULT_FONT["size_multiplier"],
        )

        self.set_original_size(500, 1080 - 150)

        self.mouse_x = 0
        self.mouse_y = 0

        self.selected_item_index = None

        # Create buttons
        margin = 25
        buttons_quantity_line = 3
        self.buttons = []
        for i in range(len(list(Item))):
            if i == 0:
                self.selected_item_index = 0

            line = i // buttons_quantity_line
            column = i % buttons_quantity_line

            self.buttons.append(
                Button(
                    margin
                    + column * (self.original_width - margin) / buttons_quantity_line,
                    margin
                    + line * (self.original_width - margin) / buttons_quantity_line,
                    (self.original_width - (buttons_quantity_line + 1) * margin)
                    / buttons_quantity_line,
                    (self.original_width - (buttons_quantity_line + 1) * margin)
                    / buttons_quantity_line,
                    content=list(Item)[i].name,
                )
            )

        # Scroll initialization
        self.scroll = 0
        line_quantity = ceil(len(list(Item)) / buttons_quantity_line)
        self.scroll_max = max(
            0,
            int(
                (
                    (self.original_width - (buttons_quantity_line + 1) * margin)
                    / buttons_quantity_line
                    + margin
                )
                * line_quantity
                + margin
                - self.original_height
            ),
        )
        self.scroll_step = 20

        self.update(data)

    def get_selected_item(self) -> Item:
        if self.selected_item_index is None:
            return None
        return list(Item)[self.selected_item_index]

    def move_buttons(self, y_value: int):
        for button in self.buttons:
            button.y += y_value

    def in_view_screen(self, point: Point) -> bool:
        return (
            point.x >= 0
            and point.x <= self.original_width
            and point.y >= 0
            and point.y <= self.original_height
        )

    def update(
        self,
        events: list[EventInstance],
        relative_mouse_position: tuple[int, int] = (0, 0),
    ):
        """
        Update the component

        Parameters:
            events (list): Events
            relative_mouse_position (tuple): Mouse position in the component
        """

        self.data = events
        self.mouse_x = relative_mouse_position[0]
        self.mouse_y = relative_mouse_position[1]

        mouse_press = False
        mouse_release = False

        for event in events:
            if event.id == Event.MOUSE_LEFT_CLICK_PRESS:
                mouse_press = True
            elif event.id == Event.MOUSE_LEFT_CLICK_RELEASE:
                mouse_release = True

            if event.id == Event.MOUSE_SCROLL_UP:
                if self.in_view_screen(Point(self.mouse_x, self.mouse_y)):
                    old_scroll = self.scroll
                    self.scroll = min(0, self.scroll + self.scroll_step)

                    if old_scroll != self.scroll:
                        self.move_buttons(self.scroll - old_scroll)

            elif event.id == Event.MOUSE_SCROLL_DOWN:
                if (
                    self.in_view_screen(Point(self.mouse_x, self.mouse_y))
                    and self.scroll_max > 0
                ):
                    old_scroll = self.scroll
                    self.scroll = max(-self.scroll_max, self.scroll - self.scroll_step)

                    if old_scroll != self.scroll:
                        self.move_buttons(self.scroll - old_scroll)

        for i in range(len(self.buttons)):
            button = self.buttons[i]

            button.update(self.mouse_x, self.mouse_y)
            if mouse_press:
                button.click_press()
            elif mouse_release:
                button.click_release()

            if button.get_state() == ButtonState.RELEASED:
                self.selected_item_index = i

        super().update()

    def render(self):
        self.surface.fill((0, 64, 0))

        for i in range(len(self.buttons)):
            button = self.buttons[i]

            button_pos = button.get_pos()
            button_state = button.get_state()
            button_content = button.get_content()

            color = (64, 64, 64)
            if button_state == ButtonState.HOVERED:
                color = (128, 128, 128)
            elif button_state == ButtonState.PRESSED:
                color = (255, 255, 255)

            if self.selected_item_index == i:
                border_size = 6
                pygame.draw.rect(
                    self.surface,
                    (192, 192, 192),
                    (
                        resize(button_pos[0] - border_size, "x"),
                        resize(button_pos[1] - border_size, "y"),
                        resize(button_pos[2] + border_size * 2, "x"),
                        resize(button_pos[3] + border_size * 2, "y"),
                    ),
                )

            pygame.draw.rect(
                self.surface,
                color,
                (
                    resize(button_pos[0], "x"),
                    resize(button_pos[1], "y"),
                    resize(button_pos[2], "x"),
                    resize(button_pos[3], "y"),
                ),
            )

            text_surface = self.text.get_surface(
                button_content,
                25,
                (255, 255, 255),
            )
            self.surface.blit(
                text_surface,
                (
                    resize(
                        button_pos[0] + button_pos[2] / 2,
                        "x",
                    )
                    - text_surface.get_width() / 2,
                    resize(
                        button_pos[1] + button_pos[3] / 2,
                        "y",
                    )
                    - text_surface.get_height() / 2,
                ),
            )

        super().render()
