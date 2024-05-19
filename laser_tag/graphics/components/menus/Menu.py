from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ..GraphicalButton import GraphicalButton


class Menu:
    def __init__(self):
        self.menu_offset_x = 0
        self.menu_offset_y = 0
        self.buttons: list[GraphicalButton] = []
        self.active: bool = True

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        for event in events:
            if event.id == Event.KEY_ESCAPE_PRESS:
                self.set_active(False)
                return

        for button in self.buttons:
            button.update(events)

    def is_active(self) -> bool:
        return self.active

    def set_active(self, active: bool):
        self.active = active
        if not self.active:
            self.deactivate_event()

    def deactivate_event(self):
        pass
