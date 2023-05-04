from ..configuration import VARIABLES
from ..entities.create_entity import create_entity
from ..entities.GameEntity import GameEntity
from ..entities.Projectile import Projectile
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
        try:
            del self.entities[uid]
        except KeyError:
            pass

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
        delta_time=DeltaTime(),
        player_delta_time: DeltaTime = None,
    ):
        if self.controlled_entity is not None or controlled_entity_id is not None:
            current_entity = (
                self.entities[self.controlled_entity]
                if self.controlled_entity is not None
                else self.entities[controlled_entity_id]
            )

            # Asynchronous mode (used by the server to process events in the past)
            async_mode = player_delta_time is not None
            player_delta_time = delta_time if not async_mode else player_delta_time

            for event in events:
                match event.id:
                    case Event.TICK:
                        # Synchonize delta time for each tick
                        if async_mode:
                            player_delta_time.update(event.timestamp)
                    case Event.GAME_ROTATE:
                        if (
                            isinstance(event.data, list)
                            and len(event.data) == 2
                            and isinstance(event.data[0], (int, float))
                        ):
                            current_entity.rotation += (
                                event.data[0] * player_delta_time.get_dt_target()
                            )
                        current_entity.rotation %= 360
                    case Event.GAME_MOVE:
                        if isinstance(event.data, (int, float)):
                            self.move_entity(
                                current_entity,
                                rotate(
                                    current_entity.move_speed
                                    * player_delta_time.get_dt_target(),
                                    current_entity.rotation + event.data,
                                ),
                            )
                    case Event.GAME_SHOOT:
                        if current_entity.attack():
                            projectile = Projectile(
                                Point(
                                    current_entity.position.x,
                                    current_entity.position.y,
                                    current_entity.position.z,
                                ),
                                self.controlled_entity
                                if self.controlled_entity is not None
                                else controlled_entity_id,
                            )
                            projectile.rotation = current_entity.rotation
                            projectile.team = current_entity.team
                            projectile.damages = current_entity.damages
                            self.spawn_entity(projectile)

            # Update other entities
            for key in list(self.entities.keys()):
                try:
                    entity = self.entities[key]
                except KeyError:
                    continue
                if isinstance(entity, Projectile):
                    collision = self.move_entity(
                        entity,
                        rotate(
                            entity.move_speed * delta_time.get_dt_target(),
                            entity.rotation,
                        ),
                    )
                    if collision:
                        self.remove_entity(key)

    def move_entity(self, entity: GameEntity, movement_vector: Point):
        collision = False

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
        else:
            collision = True

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
        else:
            collision = True

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
            else:
                collision = True

        return collision
