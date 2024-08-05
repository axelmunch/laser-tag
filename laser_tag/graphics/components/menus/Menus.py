from ....events.EventInstance import EventInstance
from .Menu import Menu


class Menus:
    """Menus manager"""

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)

            cls.__instance.init_menus()

        return cls.__instance

    def init_menus(self):
        self.menus = []
        self.menu_events = []

    def add_event(self, event: EventInstance):
        self.menu_events.append(event)

    def get_events(self) -> list[EventInstance]:
        events = self.menu_events
        self.menu_events = []
        return events

    def resize(self):
        for menu in self.menus:
            menu.resize()
            menu.update()

    def update(self, events: list[EventInstance] = []):
        """
        Update the menus

        Parameters:
            events (list): Events
        """

        # Update only the top menu
        if len(self.menus) > 0:
            self.menus[-1].update(events)

        i = 0
        while i < len(self.menus):
            if not self.menus[i].is_active():
                self.menus.pop(i)
            else:
                i += 1

    def get_menus(self) -> list[Menu]:
        return self.menus

    def open_menu(self, menu: Menu):
        menu.add_event_function = self.add_event
        self.menus.append(menu)
