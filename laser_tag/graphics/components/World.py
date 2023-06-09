from math import cos

import pygame

from ...configuration import VARIABLES
from ...entities.GameEntity import GameEntity
from ...game.Ray import Ray
from ...math.degrees_radians import degrees_to_radians
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
        Update the component.

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

    def render(self):
        self.surface.fill((42, 42, 42))

        if len(self.data["rays"]) > 0:
            step = 1920 / len(self.data["rays"])
            for i in range(len(self.data["rays"])):
                ray = self.data["rays"][i]

                ray_world_size = 0
                if ray.distance != 0:
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

                if ray.hit_point is not None:
                    pygame.draw.rect(
                        self.surface,
                        (color_intensity, color_intensity, color_intensity + 64),
                        (
                            resize(i * step - 1, "x"),
                            resize(540 - ray_world_size / 2, "y"),
                            resize(step + 2, "x"),
                            resize(ray_world_size, "y"),
                        ),
                        0,
                    )

        super().render()
