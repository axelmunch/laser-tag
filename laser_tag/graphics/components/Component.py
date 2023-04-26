import pygame

from ..resize import resize


class Component:
    """Graphical component"""

    def __init__(self, data=None):
        self.data = data
        self.surface: pygame.Surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.set_surface_size(0, 0)

    def set_surface_size(self, width, height):
        self.width = width
        self.height = height
        self.resize()

    def resize(self):
        self.surface = pygame.Surface(
            (resize(self.width, "x"), resize(self.height, "y")), pygame.SRCALPHA
        )

    def get(self) -> pygame.Surface:
        return self.surface

    def update(self, data=None):
        if data is not None:
            self.data = data
        self.render()

    def render(self):
        pass
