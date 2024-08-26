from ..configuration import VARIABLES
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..events.ServerEvents import ServerEvents
from ..utils.DeltaTime import DeltaTime
from .GameMode import GameMode
from .Mode import Mode
from .World import World


class Game:
    """Game manager"""

    def __init__(self, server_mode: bool = False):
        self.server_mode = server_mode

        self.game_mode = GameMode()
        self.world = World()
        self.server_events = ServerEvents(server_mode)

        self.mouse_x = None
        self.mouse_y = None

        self.show_scoreboard = False

        self.lock_cursor = True
        self.game_paused = False

    def __repr__(self):
        return f"[{self.game_mode},{self.world},{self.server_events}]"

    def set_state(self, parsed_object):
        try:
            self.game_mode.set_state(parsed_object["game"][0])

            controlled_entity_rotation = None
            if self.world.get_entity(self.world.controlled_entity) is not None:
                controlled_entity_rotation = self.world.get_entity(
                    self.world.controlled_entity
                ).rotation

            self.world.set_controlled_entity(int(parsed_object["controlled_entity_id"]))
            self.world.set_state(parsed_object["game"][1])

            self.server_events.set_state(parsed_object["game"][2])

            # Ignore rotation from the server
            if controlled_entity_rotation is not None:
                self.world.get_entity(self.world.controlled_entity).rotation = (
                    controlled_entity_rotation
                )

        except Exception as e:
            if VARIABLES.debug:
                print("Error setting game state", e)

    def reset(self):
        for entity in self.world.entities.values():
            entity.reset()

    def enhance_events(self, events: list[EventInstance]):
        i = 0
        while i < len(events):
            event = events[i]

            current_entity = self.world.get_entity(self.world.controlled_entity)

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
                                (
                                    0
                                    if current_entity is None
                                    else current_entity.rotation
                                    - (middle_x - self.mouse_x)
                                    * VARIABLES.rotate_sensitivity
                                    * VARIABLES.screen_width
                                    / 1920
                                ),
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

        self.game_mode.update(self.world.entities)

        for event in events:
            if event.server:
                self.server_events.add_event(event)
        self.server_events.update()
        for event in self.server_events.get_events_for_tick():
            event.local = True
            events.append(event)

        if self.server_mode and not self.game_mode.is_game_started():
            for event in events:
                match event.id:
                    case Event.START_GAME:
                        if self.game_mode.start():
                            # Reset
                            self.reset()
                    case Event.CHANGE_GAME_MODE:
                        changing_mode = Mode.SOLO
                        try:
                            changing_mode = Mode(event.data)
                        except ValueError:
                            pass

                        teams_changed = self.game_mode.change_mode(changing_mode)

                        if teams_changed:
                            self.world.reset_teams(
                                GameMode.get_teams_available(self.game_mode.game_mode)
                            )
                    case Event.CHANGE_PLAYER_TEAM:
                        self.world.change_player_team(event.data[0], event.data[1])
                    case Event.PLAYER_JOIN:
                        if self.server_mode:
                            entity = self.world.get_entity(event.data)
                            if entity is not None:
                                entity.team = GameMode.get_teams_available(
                                    self.game_mode.game_mode
                                )[0]

        self.lock_cursor = not (
            self.game_paused or not self.game_mode.is_game_started()
        )
        if self.game_paused or not self.game_mode.is_game_started():
            return

        for event in events:
            match event.id:
                case Event.KEY_ESCAPE_PRESS:
                    self.game_paused = True
                case Event.GAME_SCOREBOARD:
                    self.show_scoreboard = True
                case Event.PLAYER_JOIN:
                    if self.server_mode:
                        entity = self.world.get_entity(event.data)
                        if entity is not None:
                            entity.team = GameMode.get_teams_available(
                                self.game_mode.game_mode
                            )[0]

        self.world.update(events, controlled_entity_id, delta_time, player_delta_time)
