import pygame

from ..resize import resize


class Component:
    def __init__(self, data=None):
        self.data = data
        self.surface = None
        self.set_surface_size(0, 0)

    def set_surface_size(self, width, height):
        self.width = width
        self.height = height
        self.resize()

    def resize(self):
        self.surface = pygame.Surface(
            (resize(self.width, "x"), resize(self.height, "y"))
        )

    def get(self) -> pygame.Surface:
        return self.surface

    def update(self, data=None):
        self.data = data
        self.render()

    def render(self):
        pass
