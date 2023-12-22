from math import ceil, cos

import pygame

from ...configuration import VARIABLES
from ...entities.GameEntity import GameEntity
from ...entities.Projectile import Projectile
from ...game.Ray import Ray
from ...math.degrees_radians import degrees_to_radians
from ...math.distance import distance_points
from ...math.Point import Point
from ...math.rotations import get_angle
from ..resize import resize
from .Component import Component


class World(Component):
    """World component"""

    def __init__(
        self,
        data={"rays": [], "entities": [], "current_entity": None},
    ):
        super().__init__()

        self.set_original_size(1920, 1080)

        self.update(data["rays"], data["entities"], data["current_entity"])

    def update(
        self,
        rays: list[Ray],
        entities: list[GameEntity],
        current_entity: GameEntity = None,
    ):
        """
        Update the component

        Parameters:
            rays (list): List of rays to render
            entities (list): List of entities in the world
            current_entity (GameEntity): The current entity
        """

        self.data = {
            "rays": rays,
            "entities": entities,
            "current_entity": current_entity,
        }
        super().update()

    def position_to_screen(self, point: Point) -> float:
        # In view if value between 0 and 1

        if self.data["current_entity"] is None:
            return None

        angle_with_current_entity = (
            get_angle(point, center=self.data["current_entity"].position)
            - self.data["current_entity"].rotation
        )

        return 0.5 + angle_with_current_entity / VARIABLES.fov

    def render(self):
        self.surface.fill((42, 42, 42))

        render_list = RenderList()

        # List rays
        if len(self.data["rays"]) > 0:
            step = 1920 / len(self.data["rays"])
            for i in range(len(self.data["rays"])):
                ray = self.data["rays"][i]

                if ray.hit_point is not None:
                    render_list.add(i * step, ray.distance, ray)

        # List entities
        for entity in self.data["entities"]:
            distance = distance_points(
                self.data["current_entity"].position, entity.position
            )

            if distance > 0:
                x_position = self.position_to_screen(entity.position)
                margin = 5
                if (
                    x_position is not None
                    and x_position * 100 > -margin
                    and x_position * 100 < 100 + margin
                ):
                    render_list.add(x_position, distance, entity)

        render_queue = render_list.get()

        for element in render_queue:
            x_position = element["x_position"]
            distance = element["distance"]
            object = element["object"]

            if isinstance(object, Ray):
                ray = object

                ray_world_size = 0
                if ray.distance is not None and ray.distance != 0:
                    if self.data["current_entity"] is not None:
                        # Fix fisheye effect
                        ray_world_size = VARIABLES.world_scale / (
                            ray.distance
                            * cos(
                                degrees_to_radians(
                                    (
                                        self.data["current_entity"].rotation
                                        - ray.direction
                                    )
                                )
                            )
                        )
                    else:
                        ray_world_size = VARIABLES.world_scale / ray.distance
                ray_world_size = min(ray_world_size, 1080)

                color_intensity = 128 / max(1, ray.distance / 3)

                # Draw the ray
                pygame.draw.rect(
                    self.surface,
                    (color_intensity, color_intensity, color_intensity + 64),
                    (
                        resize(x_position, "x"),
                        resize(540 - ray_world_size / 2, "y"),
                        ceil(resize(step, "x")),
                        resize(ray_world_size, "y"),
                    ),
                    0,
                )
            elif isinstance(object, GameEntity):
                # Temporary scale
                entity_world_size = min(VARIABLES.world_scale / distance / 4, 1080)

                color = (255, 255, 255)
                if isinstance(object, Projectile):
                    entity_world_size /= 4
                    color = (0, 192, 0)

                # Draw the entity
                pygame.draw.rect(
                    self.surface,
                    color,
                    (
                        resize(
                            x_position * 1920 - entity_world_size / 2,
                            "x",
                        ),
                        resize(540 - entity_world_size / 2, "y"),
                        resize(entity_world_size, "x"),
                        resize(entity_world_size, "y"),
                    ),
                    0,
                )

        super().render()


class RenderList:
    """Render list to order elements by distance"""

    def __init__(self):
        self.list: list[dict[float, float, Ray | GameEntity]] = []

    def add(self, x_position: float, distance: float, object: Ray | GameEntity):
        self.list.append(
            {"x_position": x_position, "distance": distance, "object": object}
        )

    def sort(self):
        # Sort by greatest distance
        self.list.sort(key=lambda x: x["distance"], reverse=True)

    def get(self):
        self.sort()
        return self.list
