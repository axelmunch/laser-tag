from math import ceil

import pygame

from ...entities.GameEntity import GameEntity
from ...game.Ray import Ray
from ...math.rotations import rotate
from ..resize import resize
from .Component import Component


class Minimap(Component):
    """Minimap component"""

    def __init__(self, data={"world": [], "entities": [], "rays": []}):
        super().__init__()

        self.set_original_size(1060, 1060)

        self.update(data["world"], data["entities"], data["rays"])

    def update(
        self, world: list[list[int]], entities: list[GameEntity], rays: list[Ray] = []
    ):
        """
        Update the component.

        Parameters:
            world (grid): Map of the level as a grid
            entities (list): List of entities in the world
            rays (list): List of rays to render (optional)
        """
        self.data = {"world": world, "entities": entities, "rays": rays}
        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        map_width = 1
        map_height = len(self.data["world"])
        for y in range(map_height):
            map_width = len(self.data["world"][y])
            for x in range(map_width):
                if self.data["world"][y][x] == 1:
                    pygame.draw.rect(
                        self.surface,
                        (0, 0, 0),
                        (
                            x * self.width / map_width,
                            y * self.height / map_height,
                            ceil(self.width / map_width),
                            ceil(self.height / map_height),
                        ),
                    )

        for ray in self.data["rays"]:
            if ray.hit_point is not None:
                pygame.draw.line(
                    self.surface,
                    (255, 255, 0),
                    (
                        ray.origin.x * self.width / map_width,
                        ray.origin.y * self.height / map_height,
                    ),
                    (
                        ray.hit_point.x * self.width / map_width,
                        ray.hit_point.y * self.height / map_height,
                    ),
                    max(1, int(resize(3))),
                )

        for entity in self.data["entities"]:
            pygame.draw.rect(
                self.surface,
                (0, 128, 192),
                (
                    entity.position.x * self.width / map_width
                    - entity.collider.length / 2 * self.width / map_width,
                    entity.position.y * self.height / map_height
                    - entity.collider.width / 2 * self.height / map_height,
                    ceil(entity.collider.length * self.width / map_width),
                    ceil(entity.collider.width * self.height / map_height),
                ),
            )
            facing_direction_position = rotate(0.5, entity.rotation, entity.position)
            pygame.draw.line(
                self.surface,
                (255, 255, 255),
                (
                    entity.position.x * self.width / map_width,
                    entity.position.y * self.height / map_height,
                ),
                (
                    facing_direction_position.x * self.width / map_width,
                    facing_direction_position.y * self.height / map_height,
                ),
                max(1, int(resize(3))),
            )

        super().render()
