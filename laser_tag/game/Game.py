from ..configuration import VARIABLES
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..utils.DeltaTime import DeltaTime
from .GameMode import GameMode
from .World import World


class Game:
    """Game manager"""

    def __init__(self):
        self.game_mode = GameMode()
        self.world = World()

        self.mouse_x = None
        self.mouse_y = None

        self.show_scoreboard = False

        self.lock_cursor = True

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

    def reset(self):
        for entity in self.world.entities.values():
            entity.reset()

    def update_state(self, state):
        self.state = state

    def enhance_events(self, events: list[EventInstance]):
        i = 0
        while i < len(events):
            event = events[i]

            if event.id == Event.MOUSE_MOVE:
                self.mouse_x = event.data[0] / VARIABLES.screen_width * 1920
                self.mouse_y = event.data[1] / VARIABLES.screen_height * 1080
                event.data = [self.mouse_x, self.mouse_y]

                # Center of screen with current resolution
                middle_x = (
                    int(VARIABLES.screen_width / 2) / VARIABLES.screen_width * 1920
                )
                middle_y = (
                    int(VARIABLES.screen_height / 2) / VARIABLES.screen_height * 1080
                )

                if self.mouse_x != middle_x or self.mouse_y != middle_y:
                    events.append(
                        EventInstance(
                            Event.GAME_ROTATE,
                            [
                                -(middle_x - self.mouse_x)
                                * VARIABLES.rotate_sensitivity
                                * VARIABLES.screen_width
                                / 1920,
                                -(middle_y - self.mouse_y)
                                * VARIABLES.rotate_sensitivity
                                * VARIABLES.screen_height
                                / 1080,
                            ],
                        )
                    )

            i += 1

        self.world.enhance_events(events)

    def update(
        self,
        events: list[EventInstance],
        controlled_entity_id=None,
        delta_time=DeltaTime(),
        player_delta_time: DeltaTime = None,
    ):
        delta_time.update()

        self.show_scoreboard = False

        for event in events:
            match event.id:
                case Event.START_GAME:
                    if self.game_mode.start():
                        # Reset
                        self.reset()
                case Event.GAME_SELECT_TEAM:
                    # Can only select team if game has not started
                    if self.game_mode.game_started:
                        event.id = Event.NONE
                case Event.GAME_SCOREBOARD:
                    self.show_scoreboard = True

        self.world.update(events, controlled_entity_id, delta_time, player_delta_time)

        self.game_mode.update(self.world.entities)

        if VARIABLES.level_editor:
            self.lock_cursor = False
        else:
            self.lock_cursor = True
