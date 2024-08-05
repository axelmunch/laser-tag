from __future__ import annotations

from time import time

from .Event import Event, game_events, local_events, server_events


class EventInstance:
    """An instance of an event"""

    def __init__(self, id: Event, data=None):
        self.timestamp = time()
        self.id = id
        self.data = data
        self.local = id in local_events
        self.game = id in game_events
        self.server = id in server_events

    def __repr__(self):
        return f"[{self.id},{self.data},{self.timestamp}]"

    @staticmethod
    def create(parsed_object) -> EventInstance:
        try:
            event = EventInstance(Event(parsed_object[0]), parsed_object[1])
            event.timestamp = float(parsed_object[2])
            return event
        except:
            return None
