from ..configuration import VARIABLES
from ..entities.GameEntity import GameEntity
from ..entities.Player import Player
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..utils.DeltaTime import DeltaTime
from .GameMode import GameMode, Mode
from .World import World


class Game:
    """Game manager"""

    def __init__(self):
        self.game_mode = GameMode()
        self.world = World()

    def __repr__(self):
        return f"[{self.game_mode}, {self.world}]"

    def set_state(self, parsed_object):
        try:
            self.game_mode.set_state(parsed_object["game"][0])
            self.world.set_state(parsed_object["game"][1])
            self.world.set_controlled_entity(int(parsed_object["controlled_entity_id"]))
        except Exception as e:
            if VARIABLES.debug:
                print("Error setting game state", e)

    def update_state(self, state):
        self.state = state

    def enhance_events(self, events: list[EventInstance]):
        self.world.enhance_events(events)

    def update(
        self,
        events: list[EventInstance],
        controlled_entity_id=None,
        delta_time=DeltaTime(),
        player_delta_time: DeltaTime = None,
    ):
        delta_time.update()

        for event in events:
            match event.id:
                case Event.START_GAME:
                    self.game_mode.start()

        self.world.update(events, controlled_entity_id, delta_time, player_delta_time)

        self.game_mode.update(self.world.entities)
