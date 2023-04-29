from ..configuration import VARIABLES
from ..events.EventInstance import EventInstance
from .World import World


class Game:
    def __init__(self, map_id=None):
        self.world = World(map_id)

    def __repr__(self):
        return f"[{self.world}]"

    def set_state(self, parsed_object):
        try:
            self.world.set_state(parsed_object["game"][0])
            self.world.set_controlled_entity(int(parsed_object["controlled_entity_id"]))
        except Exception as e:
            if VARIABLES.debug:
                print("Error setting game state", e)

    def update_state(self, state):
        self.state = state

    def enhance_events(self, events: list[EventInstance]):
        self.world.enhance_events(events)

    def update(self, events: list[EventInstance]):
        self.world.update(events)
