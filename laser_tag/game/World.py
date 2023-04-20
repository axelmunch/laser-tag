from ..entities import GameEntity
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..utils.DeltaTime import DeltaTime
from .Map import Map


class World:
    def __init__(self, map_id=None):
        self.map = Map(map_id)
        self.entities = {}

        self.controlled_entity = None

        self.current_uid = 0

        self.delta_time = DeltaTime()

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
        if self.controlled_entity is not None:
            current_entity = self.entities[self.controlled_entity]

            for event in events:
                match event.id:
                    case Event.GAME_MOVE_FORWARD:
                        current_entity.move(
                            current_entity.position.x,
                            current_entity.position.y
                            - 0.1 * self.delta_time.get_dt_target(),
                            current_entity.position.z,
                        )
                    case Event.GAME_MOVE_BACKWARD:
                        current_entity.move(
                            current_entity.position.x,
                            current_entity.position.y
                            + 0.1 * self.delta_time.get_dt_target(),
                            current_entity.position.z,
                        )
                    case Event.GAME_MOVE_LEFT:
                        current_entity.move(
                            current_entity.position.x
                            - 0.1 * self.delta_time.get_dt_target(),
                            current_entity.position.y,
                            current_entity.position.z,
                        )
                    case Event.GAME_MOVE_RIGHT:
                        current_entity.move(
                            current_entity.position.x
                            + 0.1 * self.delta_time.get_dt_target(),
                            current_entity.position.y,
                            current_entity.position.z,
                        )
