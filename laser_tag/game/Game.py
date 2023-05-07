from ..configuration import VARIABLES
from ..entities.GameEntity import GameEntity
from ..entities.Player import Player
from ..events.EventInstance import EventInstance
from ..utils.DeltaTime import DeltaTime
from .World import World


class Game:
    def __init__(self):
        self.world = World()
        self.leaderboard = []

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

    def update_leaderboard(self, entities: list[GameEntity]):
        self.leaderboard.clear()
        for entity in entities.values():
            if isinstance(entity, Player):
                self.leaderboard.append([entity.eliminations, entity.team, "Name"])
        # Sort
        self.leaderboard.sort(key=lambda element: element[0], reverse=True)

    def update(
        self,
        events: list[EventInstance],
        controlled_entity_id=None,
        delta_time=DeltaTime(),
        player_delta_time: DeltaTime = None,
    ):
        delta_time.update()

        self.world.update(events, controlled_entity_id, delta_time, player_delta_time)

        self.update_leaderboard(self.world.entities)
