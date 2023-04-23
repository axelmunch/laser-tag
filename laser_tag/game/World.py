from ..configuration import VARIABLES
from ..entities.GameEntity import GameEntity
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..math.Box import Box
from ..math.Point import Point
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
                        self.move_entity(
                            current_entity,
                            Point(
                                0,
                                -0.1 * self.delta_time.get_dt_target(),
                                0,
                            ),
                        )
                    case Event.GAME_MOVE_BACKWARD:
                        self.move_entity(
                            current_entity,
                            Point(
                                0,
                                +0.1 * self.delta_time.get_dt_target(),
                                0,
                            ),
                        )
                    case Event.GAME_MOVE_LEFT:
                        self.move_entity(
                            current_entity,
                            Point(
                                -0.1 * self.delta_time.get_dt_target(),
                                0,
                                0,
                            ),
                        )
                    case Event.GAME_MOVE_RIGHT:
                        self.move_entity(
                            current_entity,
                            Point(
                                0.1 * self.delta_time.get_dt_target(),
                                0,
                                0,
                            ),
                        )
                    case Event.GAME_ROTATE:
                        current_entity.rotation += (
                            event.data[0]
                            * VARIABLES.rotate_sensitivity
                            * self.delta_time.get_dt_target()
                        )
                        current_entity.rotation %= 360

    def move_entity(self, entity: GameEntity, movement_vector: Point):
        moved_collider = Box(
            Point(
                entity.collider.origin.x + movement_vector.x,
                entity.collider.origin.y + movement_vector.y,
                entity.collider.origin.z + movement_vector.z
                if entity.collider.origin.z is not None
                else None,
            ),
            entity.collider.length,
            entity.collider.width,
            entity.collider.height,
        )

        if not self.map.collides_with(moved_collider):
            entity.move(
                entity.position.x + movement_vector.x,
                entity.position.y + movement_vector.y,
                entity.position.z + movement_vector.z
                if entity.position.z is not None
                else None,
            )
