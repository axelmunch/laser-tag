from ..entities import Entity
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from .Map import Map


class World:
    def __init__(self, map_id=None):
        self.map = Map(map_id)
        self.entities = []

        self.controlled_entity = None

    def enhance_events(self, events: list[EventInstance]):
        pass

    def update(self, events: list[EventInstance]):
        pass
