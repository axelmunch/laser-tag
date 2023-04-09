import pygame

from ..utils.DeltaTime import DeltaTime
from . import display
from .resize import resize
from .Text import Text


class Renderer:
    def __init__(self, clock: pygame.time.Clock):
        self.clock = clock
        # Load resources
        self.text = Text("calibri")

        self.delta_time = DeltaTime()
        self.x_val = 0

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

        self.text.text(
            "FPS: " + str(round(self.clock.get_fps(), 2)), 10, 10, 40, (255, 255, 255)
        )
