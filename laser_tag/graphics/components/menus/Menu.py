from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ..GraphicalElement import GraphicalElement


class Menu:
    def __init__(self):
        self.menu_offset_x = 0
        self.menu_offset_y = 0
        self.elements: list[GraphicalElement] = []
        self.active: bool = True
        self.add_event_function = None

    def resize(self):
        try:
            for element in self.elements:
                element.resize()
        except AttributeError:
            pass

    def update(self, events: list[EventInstance] = [], no_escape=False):
        """
        Update the menu

        Parameters:
            events (list): Events
        """

        for event in events:
            if not no_escape and event.id == Event.KEY_ESCAPE_PRESS:
                self.set_active(False)
                return

        for element in self.elements:
            element.update(events)

    def add_event(self, event: EventInstance):
        if self.add_event_function is not None:
            self.add_event_function(event)

    def is_active(self) -> bool:
        return self.active

    def set_active(self, active: bool):
        change_active = self.active != active
        self.active = active
        if not self.active and change_active:
            self.deactivate_event()

    def deactivate_event(self):
        pass
