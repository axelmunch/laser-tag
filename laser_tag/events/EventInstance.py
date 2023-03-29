from time import time

from .Event import Event, local_events


class EventInstance:
    def __init__(self, id: Event, data=None):
        self.timestamp = time()
        self.id = id
        self.data = data
        self.local = id in local_events
