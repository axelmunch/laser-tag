import pygame
from pygame.locals import *

from laser_tag.configuration import VARIABLES, WINDOW_WINDOWED_SIZE_RATIO
from laser_tag.events.Event import *
from laser_tag.events.get_events import *
from laser_tag.graphics import display
from laser_tag.graphics.Renderer import Renderer
from laser_tag.utils.DeltaTime import DeltaTime

if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()

    renderer = Renderer(clock)

    delta_time = DeltaTime()

    running = True

    while running:
        clock.tick(VARIABLES.fps)

        delta_time.update()

        # Events
        events = get_events()

        # Process events
        for event in events:
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
        renderer.render()

        pygame.display.flip()

    pygame.quit()
