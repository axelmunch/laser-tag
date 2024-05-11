from math import ceil

from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....math.Point import Point
from ...Button import ButtonState
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import ButtonType, GraphicalButton
from .Item import Item


class ItemMenu(Component):
    """Level editor item menu component"""

    def __init__(self):
        super().__init__()

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
                GraphicalButton(
                    margin
                    + column * (self.original_width - margin) / buttons_quantity_line,
                    margin
                    + line * (self.original_width - margin) / buttons_quantity_line,
                    (self.original_width - (buttons_quantity_line + 1) * margin)
                    / buttons_quantity_line,
                    (self.original_width - (buttons_quantity_line + 1) * margin)
                    / buttons_quantity_line,
                    content=list(Item)[i].name,
                    type=ButtonType.LEVEL_EDITOR_ITEM,
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

        self.update()

    def resize(self):
        super().resize()

        try:
            for button in self.buttons:
                button.resize()
        except AttributeError:
            pass

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
        events: list[EventInstance] = [],
        relative_offset: tuple[int, int] = (0, 0),
    ):
        """
        Update the component

        Parameters:
            events (list): Events
            relative_offset (tuple): Component position on the screen
        """

        for event in events:
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

            elif event.id == Event.MOUSE_MOVE:
                self.mouse_x = event.data[0] - relative_offset[0]
                self.mouse_y = event.data[1] - relative_offset[1]

        for i in range(len(self.buttons)):
            button = self.buttons[i]
            button.set_relative_offset(relative_offset[0], relative_offset[1])
            button.update(events)
            if button.get_state() == ButtonState.RELEASED:
                self.selected_item_index = i
            button.set_selected(self.selected_item_index == i)

        super().update()

    def render(self):
        self.surface.fill((0, 64, 0))

        for button in self.buttons:
            self.surface.blit(
                button.get(),
                (resize(button.x, "x"), resize(button.y, "y")),
            )

        super().render()
