from ..entities import GameEntity
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from .Map import Map


class World:
    def __init__(self, map_id=None):
        self.map = Map(map_id)
        self.entities = {}

        self.controlled_entity = None

        self.current_uid = 0

    def get_uid(self):
        uid = self.current_uid
        self.current_uid += 1
        return uid

    def spawn_entity(self, entity: GameEntity):
        self.entities[self.get_uid()] = entity
        return self.current_uid - 1

    def set_controlled_entity(self, uid):
        self.controlled_entity = uid

    def enhance_events(self, events: list[EventInstance]):
        pass

    def update(self, events: list[EventInstance]):
        pass
