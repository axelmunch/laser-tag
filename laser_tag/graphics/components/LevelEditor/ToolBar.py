import pygame

from ....configuration import DEFAULT_FONT
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ...resize import resize
from ...Text import Text
from ..Component import Component


class ToolBar(Component):
    """Level editor tool bar component"""

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

        self.set_original_size(1920, 150)

        self.mouse_x = 0
        self.mouse_y = 0

        self.update(data)

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

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0))

        super().render()
