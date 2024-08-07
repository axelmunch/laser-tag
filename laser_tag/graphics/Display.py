from os import makedirs
from time import strftime, time

import pygame
from pygame.locals import *

from ..configuration import SCREENSHOTS_PATH, VARIABLES


class Display:
    def __init__(self):
        self.screen: pygame.Surface = None

        self.refresh_display()

    def refresh_display(self, free_aspect_ratio=False):
        if VARIABLES.fullscreen:
            VARIABLES.set_screen_size(
                VARIABLES.full_screen_width, VARIABLES.full_screen_height
            )
        else:
            if not free_aspect_ratio:
                # Default window size
                VARIABLES.set_screen_size(
                    int(
                        VARIABLES.full_screen_width
                        * VARIABLES.windowed_resolution_ratio
                    ),
                    int(
                        VARIABLES.full_screen_height
                        * VARIABLES.windowed_resolution_ratio
                    ),
                )

        self.screen = pygame.display.set_mode(
            (VARIABLES.screen_width, VARIABLES.screen_height),
            FULLSCREEN if VARIABLES.fullscreen else RESIZABLE,
        )

    def screenshot(self):
        makedirs(SCREENSHOTS_PATH, exist_ok=True)

        time_string = strftime(f"%Y-%m-%d_%H.%M.%S.{int(round(time() * 1000) % 1000)}")

        screenshot_file = SCREENSHOTS_PATH.joinpath(f"screenshot_{time_string}.png")

        pygame.image.save(self.screen, screenshot_file)

        if VARIABLES.debug:
            print(f"Screenshot saved: {screenshot_file}")
