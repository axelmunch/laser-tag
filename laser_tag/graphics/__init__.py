import pygame
from pygame.locals import *

from ..configuration import GAME_NAME, VARIABLES
from .Display import Display

pygame.init()

pygame.display.set_caption(GAME_NAME)

# Set screen size
VARIABLES.set_full_screen_size(
    pygame.display.Info().current_w, pygame.display.Info().current_h
)

display = Display()
display.refresh_display()
