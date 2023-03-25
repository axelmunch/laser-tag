from time import time

import pygame
from pygame.locals import *

from laser_tag.configuration import TARGET_FPS, VARIABLES, WINDOW_WINDOWED_SIZE_RATIO
from laser_tag.graphics import display
from laser_tag.graphics.resize import resize

if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Calibri", 20)

    previous_time = time()
    x_val = 0

    running = True

    while running:
        clock.tick(VARIABLES.fps)

        current_time = time()
        dt = current_time - previous_time
        dt_target = dt * TARGET_FPS
        previous_time = current_time

        x_val += 10 * dt_target
        x_val %= 1920

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
            (
                resize(15 + x_val, "x"),
                resize(15, "y"),
                resize(125, "x"),
                resize(125, "y"),
            ),
        )

        fps_text = font.render(
            "FPS: " + str(round(clock.get_fps(), 2)), True, (255, 255, 255)
        )
        display.screen.blit(fps_text, (resize(15, "x"), resize(15, "y")))

        pygame.display.flip()

    pygame.quit()
