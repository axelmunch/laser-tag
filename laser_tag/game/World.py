from math import atan
from threading import Lock

from ..configuration import GAME_WORLD_FILE, VARIABLES
from ..entities.create_entity import create_entity
from ..entities.GameEntity import GameEntity
from ..entities.LaserRay import LaserRay
from ..entities.Player import Player
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..game.Ray import Ray
from ..math.Circle import Circle
from ..math.degrees_radians import radians_to_degrees
from ..math.Point import Point
from ..math.rotations import get_angle, rotate
from ..utils.DeltaTime import DeltaTime
from .load_world import load_world
from .Map import Map
from .Team import Team


class World:
    """World class, contains all entities and map"""

    def __init__(self):
        self.map = Map()
        self.entities: dict[int, GameEntity] = {}

        self.controlled_entity = None

        self.current_uid = 0
        self.uid_mutex = Lock()

        self.load_world(GAME_WORLD_FILE)

    def __repr__(self):
        return f"{self.entities}"

    def set_state(self, parsed_object):
        self.entities.clear()
        try:
            for key in parsed_object:
                new_entity = create_entity(parsed_object[key])
                if new_entity is not None:
                    # Specific case for LaserRay
                    if isinstance(new_entity, LaserRay):
                        new_entity.get_entity_fct = self.get_entity

                    self.entities[key] = new_entity
        except Exception as e:
            if VARIABLES.debug:
                print("Error setting world state", e)

    def load_world(self, world_file):
        world_data = load_world(world_file)

        self.map.set_walls(world_data["walls"])
        self.entities = {}
        for entity in world_data["entities"]:
            self.spawn_entity(entity)

        self.map.spawn_points = world_data["spawn_points"]

    def get_uid(self):
        self.uid_mutex.acquire()
        self.current_uid += 1
        uid = self.current_uid
        self.uid_mutex.release()
        return uid

    def spawn_entity(self, entity: GameEntity):
        self.entities[self.get_uid()] = entity
        return self.current_uid

    def get_entity(self, uid) -> GameEntity | None:
        try:
            return self.entities[uid]
        except KeyError:
            return None

    def remove_entity(self, uid):
        try:
            del self.entities[uid]
        except KeyError:
            pass

    def set_controlled_entity(self, uid):
        self.controlled_entity = uid

    def change_player_team(self, id, team: Team):
        try:
            team = Team(team)
        except ValueError:
            pass
        player = self.get_entity(id)
        if player is not None:
            player.team = team

    def reset_teams(self, teams: list[Team]):
        index = 0
        for entity in self.entities.values():
            if isinstance(entity, Player):
                entity.team = teams[index % len(teams)]
                index += 1

    def get_current_position(self) -> Point | None:
        entity = self.get_entity(self.controlled_entity)
        return entity.position if entity is not None else None

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
                self.get_entity(self.controlled_entity)
                if self.controlled_entity is not None
                else self.get_entity(controlled_entity_id)
            )

            if current_entity is None:
                if VARIABLES.debug:
                    print("Invalid controlled entity")
                return

            # Asynchronous mode (used by the server to process events in the past)
            async_mode = player_delta_time is not None
            player_delta_time = delta_time if not async_mode else player_delta_time

            is_moving = False
            is_running = False

            for event in events:
                match event.id:
                    case Event.GAME_RUN:
                        is_running = True
                    case Event.GAME_MOVE:
                        is_moving = True

            current_entity.is_moving = is_moving
            current_entity.is_running = is_moving and is_running
            current_entity.is_crouching = False
            current_entity.holding_restart = False

            for event in events:
                match event.id:
                    case Event.TICK:
                        # Synchonize delta time for each tick
                        if async_mode:
                            player_delta_time.update(event.timestamp)
                    case Event.GAME_CROUCH:
                        current_entity.is_crouching = True
                        current_entity.is_running = False
                    case Event.GAME_ROTATE:
                        if (
                            isinstance(event.data, list)
                            and len(event.data) == 2
                            and isinstance(event.data[0], (float, int))
                        ):
                            current_entity.rotation = event.data[0] % 360
                    case Event.GAME_MOVE:
                        if isinstance(event.data, (float, int)):
                            self.move_entity(
                                current_entity,
                                rotate(
                                    current_entity.move_speed
                                    * (
                                        current_entity.run_speed_multiplier
                                        if current_entity.is_running
                                        else 1
                                    )
                                    * (
                                        current_entity.crouch_speed_multiplier
                                        if current_entity.is_crouching
                                        else 1
                                    )
                                    * player_delta_time.get_dt_target(),
                                    current_entity.rotation + event.data,
                                ),
                            )
                    case Event.GAME_SHOOT:
                        current_entity.holding_restart = True

                        if current_entity.attack():
                            ray = self.map.cast_ray(
                                current_entity.position,
                                (current_entity.rotation) % 360,
                            )
                            end_position = current_entity.position
                            if ray.hit_point is not None:
                                end_position = ray.hit_point

                            laser_ray = LaserRay(
                                Point(
                                    current_entity.position.x, current_entity.position.y
                                ),
                                end_position,
                                (
                                    self.controlled_entity
                                    if self.controlled_entity is not None
                                    else controlled_entity_id
                                ),
                            )
                            laser_ray.rotation = current_entity.rotation
                            laser_ray.team = current_entity.team
                            laser_ray.damages = current_entity.damages
                            laser_ray.get_entity_fct = self.get_entity
                            self.spawn_entity(laser_ray)

            # The player is shooting if there is a laser ray with his id
            current_entity.is_shooting = False
            for entity in self.entities.values():
                if isinstance(entity, LaserRay):
                    if entity.parent_id == (
                        self.controlled_entity
                        if self.controlled_entity is not None
                        else controlled_entity_id
                    ):
                        current_entity.is_shooting = True
                        break

            # Update other entities
            for key in list(self.entities.keys()):
                entity = self.get_entity(key)
                if entity is None:
                    continue
                # Remove dead entities
                if not entity.alive:
                    self.remove_entity(key)
                    continue

                # Laser ray
                if isinstance(entity, LaserRay):
                    # Collision with entities
                    if entity.can_attack:
                        for key_target in list(self.entities.keys()):
                            entity_target = self.get_entity(key_target)
                            # Target is not the laser ray nor its parent
                            if (
                                entity_target is None
                                or key == key_target
                                or entity.parent_id == key_target
                            ):
                                continue
                            # Target is in a different team (or not in a team)
                            if (
                                entity.team != entity_target.team
                                or entity_target.team == Team.NONE
                            ):
                                # Collision with the target
                                if (
                                    entity_target.check_can_be_attacked()
                                    and entity.collides_with(entity_target)
                                    and entity.attack()
                                ):
                                    entity.can_attack = False
                                    # Damage the target
                                    killed = entity_target.damage(entity.damages)
                                    # The target was hit
                                    if killed is not None:
                                        entity.on_hit(entity_target)
                                        if killed:
                                            entity.on_kill(entity_target)

                    entity.time_to_live -= delta_time.get_dt()
                    if entity.time_to_live <= 0:
                        entity.death()

    def move_entity(self, entity: GameEntity, movement_vector: Point) -> bool:
        new_entity_position = Point(entity.position.x, entity.position.y)
        collision = False

        # X
        moved_collider_x = Circle(
            Point(
                entity.collider.origin.x + movement_vector.x, entity.collider.origin.y
            ),
            entity.collider.radius,
        )

        if not self.map.collides_with(moved_collider_x):
            new_entity_position.x += movement_vector.x
        else:
            collision = True

        # Y
        moved_collider_y = Circle(
            Point(
                entity.collider.origin.x, entity.collider.origin.y + movement_vector.y
            ),
            entity.collider.radius,
        )

        if not self.map.collides_with(moved_collider_y):
            new_entity_position.y += movement_vector.y
        else:
            collision = True

        entity.move(new_entity_position.x, new_entity_position.y)

        return collision

    def cast_rays(self) -> list[tuple[int, Ray]]:
        rays: list[tuple[int, Ray]] = []

        entity = self.get_entity(self.controlled_entity)

        if entity is not None:
            for i in range(VARIABLES.rays_quantity):
                # Even ray distribution
                normalized_distance = i / VARIABLES.rays_quantity * 2 - 1  # -1 to 1
                ray_rotation = radians_to_degrees(atan(normalized_distance))
                ray_rotation = ray_rotation / 90 * VARIABLES.fov

                ray = self.map.cast_ray(
                    entity.position,
                    (entity.rotation + ray_rotation) % 360,
                )
                if ray.distance != 0:
                    rays.append((i, ray))

        return rays
