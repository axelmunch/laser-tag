from math import sin
from time import time

from ...events.EventInstance import EventInstance
from .Component import Component


class BackgroundMenu(Component):
    """Background menu component"""

    def __init__(self):
        super().__init__()

        self.set_original_size(1920, 1080)

        self.update()

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        super().update()

    def render(self):
        self.surface.fill((130, 100, (sin(time() / 2) + 1) * 50))

        super().render()
