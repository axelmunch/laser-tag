from math import ceil

import pygame

from ...configuration import VARIABLES
from ..resize import resize


class Component:
    """Graphical component"""

    def __init__(self, data=None):
        self.data = data
        self.surface: pygame.Surface
        self.set_original_size(0, 0)

    def set_original_size(self, width: int, height: int):
        self.original_width = width
        self.original_height = height
        self.resize()

    def get_size(self) -> tuple[int, int]:
        return self.original_width, self.original_height

    def set_surface_size(self, width, height):
        self.width = ceil(width)
        self.height = ceil(height)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def resize(self):
        self.set_surface_size(
            resize(self.original_width, "x"), resize(self.original_height, "y")
        )

    def get(self) -> pygame.Surface:
        return self.surface

    def update(self, data=None):
        if data is not None:
            self.data = data
        self.render()

    def render(self):
        if VARIABLES.show_components_outline:
            pygame.draw.rect(
                self.surface, (0, 255, 0), (0, 0, self.width, self.height), 1
            )
