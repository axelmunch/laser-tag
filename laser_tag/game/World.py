from ..configuration import VARIABLES
from ..entities.create_entity import create_entity
from ..entities.GameEntity import GameEntity
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..math.Box import Box
from ..math.Point import Point
from ..math.rotations import get_angle, rotate
from ..utils.DeltaTime import DeltaTime
from .Map import Map


class World:
    def __init__(self):
        self.map = Map()
        self.entities = {}

        self.controlled_entity = None

        self.current_uid = 0

        self.delta_time = DeltaTime()

    def __repr__(self):
        return f"{self.entities}"

    def set_state(self, parsed_object):
        self.entities.clear()
        try:
            for entity in parsed_object:
                new_entity = create_entity(parsed_object[entity])
                if new_entity is not None:
                    self.entities[int(entity)] = new_entity
        except Exception as e:
            if VARIABLES.debug:
                print("Error setting world state", e)

    def get_uid(self):
        self.current_uid += 1
        uid = self.current_uid
        return uid

    def spawn_entity(self, entity: GameEntity):
        self.entities[self.get_uid()] = entity
        return self.current_uid

    def remove_entity(self, uid):
        del self.entities[uid]

    def set_controlled_entity(self, uid):
        self.controlled_entity = uid

    def enhance_events(self, events: list[EventInstance]):
        movement_vector = [0, 0]

        i = 0
        while i < len(events):
            event = events[i]

            if event.id == Event.GAME_MOVE_FORWARD:
                movement_vector[0] += 1
            if event.id == Event.GAME_MOVE_BACKWARD:
                movement_vector[0] -= 1
            if event.id == Event.GAME_MOVE_LEFT:
                movement_vector[1] -= 1
            if event.id == Event.GAME_MOVE_RIGHT:
                movement_vector[1] += 1

            i += 1

        # Movement direction
        if movement_vector[0] != 0 or movement_vector[1] != 0:
            events.append(
                EventInstance(
                    Event.GAME_MOVE,
                    get_angle(
                        Point(
                            movement_vector[0],
                            movement_vector[1],
                        )
                    ),
                )
            )

    def update(
        self,
        events: list[EventInstance],
        controlled_entity_id=None,
        delta_time: DeltaTime = None,
    ):
        if self.controlled_entity is not None or controlled_entity_id is not None:
            current_entity = (
                self.entities[self.controlled_entity]
                if self.controlled_entity is not None
                else self.entities[controlled_entity_id]
            )

            if delta_time is None:
                delta_time = self.delta_time

            for event in events:
                match event.id:
                    case Event.GAME_ROTATE:
                        current_entity.rotation += (
                            event.data[0]
                            * VARIABLES.rotate_sensitivity
                            * delta_time.get_dt_target()
                        )
                        current_entity.rotation %= 360
                    case Event.GAME_MOVE:
                        self.move_entity(
                            current_entity,
                            rotate(
                                current_entity.move_speed * delta_time.get_dt_target(),
                                current_entity.rotation + event.data,
                            ),
                        )

    def move_entity(self, entity: GameEntity, movement_vector: Point):
        moved_collider_x = Box(
            Point(
                entity.collider.origin.x + movement_vector.x,
                entity.collider.origin.y,
                entity.collider.origin.z,
            ),
            entity.collider.length,
            entity.collider.width,
            entity.collider.height,
        )

        if not self.map.collides_with(moved_collider_x):
            entity.move(
                entity.position.x + movement_vector.x,
                entity.position.y,
                entity.position.z,
            )

        moved_collider_y = Box(
            Point(
                entity.collider.origin.x,
                entity.collider.origin.y + movement_vector.y,
                entity.collider.origin.z,
            ),
            entity.collider.length,
            entity.collider.width,
            entity.collider.height,
        )

        if not self.map.collides_with(moved_collider_y):
            entity.move(
                entity.position.x,
                entity.position.y + movement_vector.y,
                entity.position.z,
            )

        if entity.collider.origin.z is not None and movement_vector.z is not None:
            moved_collider_z = Box(
                Point(
                    entity.collider.origin.x,
                    entity.collider.origin.y,
                    entity.collider.origin.z + movement_vector.z,
                ),
                entity.collider.length,
                entity.collider.width,
                entity.collider.height,
            )

            if not self.map.collides_with(moved_collider_z):
                entity.move(
                    entity.position.x,
                    entity.position.y,
                    entity.position.z + movement_vector.z,
                )
