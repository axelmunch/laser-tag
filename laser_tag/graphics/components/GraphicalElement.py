from ...events.EventInstance import EventInstance
from .Component import Component


class GraphicalElement(Component):
    def __init__(self):
        super().__init__()
        self.selected: bool = False

    def is_selected(self) -> bool:
        return self.selected

    def set_selected(self, selected: bool):
        self.selected = selected

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        super().update()

    def render(self):
        super().render()
