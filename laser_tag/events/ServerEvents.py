from __future__ import annotations

from time import time

from ..configuration import SERVER_EVENTS_LIFESPAN
from .EventInstance import EventInstance


class ServerEvents:
    """Events from the server to play only once"""

    def __init__(self, server_mode: bool = True):
        self.server_mode = server_mode

        self.events: dict[int, EventInstance] = {}
        # Events for the current tick
        self.tick_events = []

        self.server_id = 1
        self.client_id = 0

    def add_event(self, event: EventInstance):
        if self.server_mode:
            # Update timestamp to now
            event.timestamp = time()

            self.events[self.server_id] = event
            self.server_id += 1

    def get_events_to_send(self) -> dict[int, EventInstance]:
        if self.server_mode:
            # Delete events older than limit
            for id in list(self.events.keys()):
                if time() - self.events[id].timestamp > SERVER_EVENTS_LIFESPAN:
                    del self.events[id]

        return self.events

    def update(self) -> list[EventInstance]:
        self.tick_events = []

        for id in self.events:
            if id > self.client_id:
                if isinstance(self.events[id], EventInstance):
                    self.tick_events.append(self.events[id])
                else:
                    created_event = EventInstance.create(self.events[id])
                    if created_event is not None:
                        self.tick_events.append(created_event)

        self.client_id = max([self.client_id] + list(self.events.keys()))

        return self.tick_events

    def get_events_for_tick(self) -> list[EventInstance]:
        return self.tick_events

    def __repr__(self):
        return f"[{self.get_events_to_send()},{self.server_id}]"

    def set_state(self, parsed_object):
        self.events = parsed_object[0]

        if parsed_object[1] < self.client_id:
            self.client_id = 0
