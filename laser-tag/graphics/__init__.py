import pygame
from pygame.locals import *

from ..configuration import GAME_NAME, VARIABLES, WINDOW_WINDOWED_SIZE_RATIO

pygame.init()

pygame.display.set_caption(GAME_NAME)

VARIABLES.set_full_screen_size(
    pygame.display.Info().current_w, pygame.display.Info().current_h
)
VARIABLES.set_screen_size(
    int(VARIABLES.screen_width * WINDOW_WINDOWED_SIZE_RATIO),
    int(VARIABLES.screen_height * WINDOW_WINDOWED_SIZE_RATIO),
)


class Display:
    def __init__(self):
        self.screen = None

        self.clock = pygame.time.Clock()

        self.refresh_screen()

    def refresh_screen(self):
        self.screen = pygame.display.set_mode(
            (VARIABLES.screen_width, VARIABLES.screen_height),
            FULLSCREEN if VARIABLES.fullscreen else RESIZABLE,
        )


display = Display()
