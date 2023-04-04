from time import time

from ..network.safe_eval import safe_eval
from .Event import Event, local_events


class EventInstance:
    def __init__(self, id: Event, data=None):
        self.timestamp = time()
        self.id = id
        self.data = data
        self.local = id in local_events
        self.quantity = 1
        self.time_pressed = 0

    def __repr__(self):
        return f"[{self.id.value}, {self.data}, {self.quantity}, {self.time_pressed}]"

    @staticmethod
    def create(string):
        parsed_event = safe_eval(string)
        try:
            event = EventInstance(Event(parsed_event[0]), parsed_event[1])
            event.quantity = parsed_event[2]
            event.time_pressed = parsed_event[3]
            return event
        except:
            return None
