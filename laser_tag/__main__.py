from time import time

import pygame
from pygame.locals import *

from laser_tag.configuration import TARGET_FPS, VARIABLES, WINDOW_WINDOWED_SIZE_RATIO
from laser_tag.events.Event import *
from laser_tag.events.get_events import *
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
        for event in get_events():
            match event.id:
                case Event.WINDOW_QUIT:
                    running = False
                    break
                case Event.KEY_ESCAPE_PRESS:
                    running = False
                case Event.WINDOW_FULLSCREEN:
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
                case Event.WINDOW_RESIZE:
                    if not VARIABLES.fullscreen:
                        VARIABLES.set_screen_size(event.data[0], event.data[1])
                        display.refresh_display()

                case Event.MOUSE_MOVE:
                    mouse_x = event.data[0] / VARIABLES.screen_width * 1920
                    mouse_y = event.data[1] / VARIABLES.screen_height * 1080
                    # print(mouse_x, mouse_y)

                case Event.MOUSE_LEFT_CLICK_PRESS:
                    print("CLICK")

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
