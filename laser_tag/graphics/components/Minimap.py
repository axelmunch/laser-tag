from math import ceil

import pygame

from .Component import Component


class Minimap(Component):
    def __init__(self, data=[]):
        super().__init__()

        self.set_surface_size(400, 400)

        self.update(data)

    def update(self, world):
        """
        Update the component.

        Parameters:
            world (grid): Map of the level as a grid
        """
        self.data = world
        super().update()

    def render(self):
        surface_width = self.surface.get_width()
        surface_height = self.surface.get_height()
        map_height = len(self.data)
        for y in range(map_height):
            map_width = len(self.data[y])
            for x in range(map_width):
                if self.data[y][x] == 1:
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
