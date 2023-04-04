import pygame
from pygame.locals import *

from ..configuration import VARIABLES


class Display:
    def __init__(self):
        self.screen: pygame.Surface = None

        self.refresh_display()

    def refresh_display(self):
        self.screen = pygame.display.set_mode(
            (VARIABLES.screen_width, VARIABLES.screen_height),
            FULLSCREEN if VARIABLES.fullscreen else RESIZABLE,
        )
