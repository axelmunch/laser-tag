from ..events.EventInstance import EventInstance
from .World import World


class Game:
    def __init__(self, map_id=None):
        self.world = World(map_id)

    def update_state(self, state):
        self.state = state

    def enhance_events(self, events: list[EventInstance]):
        self.world.enhance_events(events)

    def update(self, events: list[EventInstance]):
        self.world.update(events)
