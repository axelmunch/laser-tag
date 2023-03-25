import pygame
from pygame.locals import *

from ..configuration import GAME_NAME, VARIABLES, WINDOW_WINDOWED_SIZE_RATIO
from .Display import Display

pygame.init()

pygame.display.set_caption(GAME_NAME)

# Set screen size
VARIABLES.set_full_screen_size(
    pygame.display.Info().current_w, pygame.display.Info().current_h
)
# Default window size
VARIABLES.set_screen_size(
    int(VARIABLES.screen_width * WINDOW_WINDOWED_SIZE_RATIO),
    int(VARIABLES.screen_height * WINDOW_WINDOWED_SIZE_RATIO),
)

display = Display()
