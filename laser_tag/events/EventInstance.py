from __future__ import annotations

from time import time

from ..network.safe_eval import safe_eval
from .Event import Event, local_events


class EventInstance:
    """An instance of an event"""

    def __init__(self, id: Event, data=None):
        self.timestamp = time()
        self.id = id
        self.data = data
        self.local = id in local_events

    def __repr__(self):
        return f"[{self.id}, {self.data}, {self.timestamp}]"

    @staticmethod
    def create(parsed_object) -> EventInstance:
        try:
            event = EventInstance(Event(parsed_object[0]), parsed_object[1])
            event.timestamp = float(parsed_object[2])
            return event
        except:
            return None
