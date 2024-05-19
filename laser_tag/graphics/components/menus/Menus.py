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
            if not self.menus[-1].is_active():
                self.menus.pop(-1)

    def get_menus(self) -> list[Menu]:
        return self.menus

    def open_menu(self, menu: Menu):
        self.menus.append(menu)
