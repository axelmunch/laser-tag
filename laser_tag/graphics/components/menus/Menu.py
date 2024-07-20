from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ..GraphicalElement import GraphicalElement


class Menu:
    def __init__(self):
        self.menu_offset_x = 0
        self.menu_offset_y = 0
        self.elements: list[GraphicalElement] = []
        self.active: bool = True

    def resize(self):
        try:
            for element in self.elements:
                element.resize()
        except AttributeError:
            pass

    def update(self, events: list[EventInstance] = []):
        """
        Update the menu

        Parameters:
            events (list): Events
        """

        for event in events:
            if event.id == Event.KEY_ESCAPE_PRESS:
                self.set_active(False)
                return

        for element in self.elements:
            element.update(events)

    def is_active(self) -> bool:
        return self.active

    def set_active(self, active: bool):
        change_active = self.active != active
        self.active = active
        if not self.active and change_active:
            self.deactivate_event()

    def deactivate_event(self):
        pass
