import pygame

from ..configuration import VARIABLES
from ..game.Game import Game
from ..utils.DeltaTime import DeltaTime
from . import display
from .components.Fps import Fps
from .components.Minimap import Minimap
from .resize import resize


class Renderer:
    def __init__(self, clock: pygame.time.Clock):
        self.clock = clock
        # Load resources

        self.fps = Fps()
        self.minimap = Minimap()
        self.components = [self.fps, self.minimap]

    def resize(self):
        for component in self.components:
            component.resize()

    def render(self, game: Game):
        # Update display
        display.screen.fill((42, 42, 42))

        self.minimap.update(game.world.map.map, game.world.entities.values())
        display.screen.blit(self.minimap.get(), (resize(10, "x"), resize(10, "y")))

        if VARIABLES.show_fps:
            self.fps.update(self.clock.get_fps())
            display.screen.blit(self.fps.get(), (resize(10, "x"), resize(10, "y")))
