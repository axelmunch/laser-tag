from math import ceil

import pygame

from .Component import Component


class Minimap(Component):
    def __init__(self, data={"world": [], "entities": []}):
        super().__init__()

        self.set_surface_size(1060, 1060)

        self.update(data["world"], data["entities"])

    def update(self, world, entities):
        """
        Update the component.

        Parameters:
            world (grid): Map of the level as a grid
            entities (list): List of entities in the world
        """
        self.data = {"world": world, "entities": entities}
        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        surface_width = self.surface.get_width()
        surface_height = self.surface.get_height()
        map_height = len(self.data["world"])
        for y in range(map_height):
            map_width = len(self.data["world"][y])
            for x in range(map_width):
                if self.data["world"][y][x] == 1:
                    pygame.draw.rect(
                        self.surface,
                        (0, 0, 0),
                        (
                            x * surface_width / map_width,
                            y * surface_height / map_height,
                            ceil(surface_width / map_width),
                            ceil(surface_height / map_height),
                        ),
                    )
        for entity in self.data["entities"]:
            pygame.draw.rect(
                self.surface,
                (0, 128, 192),
                (
                    entity.position.x * surface_width / map_width
                    - entity.collider.length / 2 * surface_width / map_width,
                    entity.position.y * surface_height / map_height
                    - entity.collider.width / 2 * surface_height / map_height,
                    ceil(entity.collider.length * surface_width / map_width),
                    ceil(entity.collider.width * surface_height / map_height),
                ),
            )
