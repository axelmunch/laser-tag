import pygame

from ..utils.DeltaTime import DeltaTime
from . import display
from .components.Fps import Fps
from .resize import resize


class Renderer:
    def __init__(self, clock: pygame.time.Clock):
        self.clock = clock
        # Load resources

        self.delta_time = DeltaTime()

        self.fps = Fps()
        self.components = [self.fps]

        self.x_val = 0

    def resize(self):
        for component in self.components:
            component.resize()

    def render(self):
        # Moving object test
        self.x_val += 10 * self.delta_time.get_dt_target()
        self.x_val %= 1920

        # Update display
        display.screen.fill((42, 42, 42))

        pygame.draw.rect(
            display.screen,
            (0, 128, 0),
            (
                resize(15 + self.x_val, "x"),
                resize(15, "y"),
                resize(125, "x"),
                resize(125, "y"),
            ),
        )

        self.fps.update(self.clock.get_fps())
        display.screen.blit(self.fps.get(), (resize(10, "x"), resize(10, "y")))
