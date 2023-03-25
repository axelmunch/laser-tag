import pygame
from pygame.locals import *

from laser_tag.configuration import VARIABLES, WINDOW_WINDOWED_SIZE_RATIO
from laser_tag.graphics import display
from laser_tag.graphics.resize import resize

if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(VARIABLES.fps)

        # Events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_F11:
                    VARIABLES.fullscreen = not VARIABLES.fullscreen
                    if VARIABLES.fullscreen:
                        VARIABLES.set_screen_size(
                            VARIABLES.full_screen_width, VARIABLES.full_screen_height
                        )
                    else:
                        VARIABLES.set_screen_size(
                            int(VARIABLES.screen_width * WINDOW_WINDOWED_SIZE_RATIO),
                            int(VARIABLES.screen_height * WINDOW_WINDOWED_SIZE_RATIO),
                        )
                    display.refresh_display()
            elif event.type == pygame.VIDEORESIZE:
                if not VARIABLES.fullscreen:
                    VARIABLES.set_screen_size(event.w, event.h)
                    display.refresh_display()

        # Display
        display.screen.fill((42, 42, 42))

        pygame.draw.rect(
            display.screen,
            (0, 128, 0),
            (resize(15, "x"), resize(15, "y"), resize(125, "x"), resize(125, "y")),
        )

        pygame.display.flip()

    pygame.quit()
