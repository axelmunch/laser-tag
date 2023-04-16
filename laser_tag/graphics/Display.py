from os import makedirs
from time import strftime, time

import pygame
from pygame.locals import *

from ..configuration import SCREENSHOTS_PATH, VARIABLES


class Display:
    def __init__(self):
        self.screen: pygame.Surface = None

        self.refresh_display()

    def refresh_display(self):
        self.screen = pygame.display.set_mode(
            (VARIABLES.screen_width, VARIABLES.screen_height),
            FULLSCREEN if VARIABLES.fullscreen else RESIZABLE,
        )

    def screenshot(self):
        makedirs(SCREENSHOTS_PATH, exist_ok=True)

        time_string = strftime(f"%Y-%m-%d_%H.%M.%S.{int(round(time() * 1000) % 1000)}")

        screenshot_file_name = f"{SCREENSHOTS_PATH}/screenshot_{time_string}.png"

        pygame.image.save(self.screen, screenshot_file_name)

        if VARIABLES.debug:
            print(f"Screenshot saved: {screenshot_file_name}")
