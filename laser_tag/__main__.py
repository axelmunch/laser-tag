import pygame
from pygame.locals import *

from laser_tag.configuration import VARIABLES, WINDOW_WINDOWED_SIZE_RATIO
from laser_tag.events.Event import Event
from laser_tag.events.get_events import *
from laser_tag.game.Game import Game
from laser_tag.graphics import display
from laser_tag.graphics.Renderer import Renderer
from laser_tag.network.Client import Client
from laser_tag.network.Server import Server

if __name__ == "__main__":
    pygame.init()

    game = Game()

    clock = pygame.time.Clock()

    renderer = Renderer(clock)

    # Local server
    server = Server(0, debug=True)
    server.start()

    client = Client("localhost", server.get_port())

    running = True

    while running:
        clock.tick(VARIABLES.fps)

        # Events
        events = get_events()

        # Enhance events
        game.enhance_events(events)

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
                    renderer.resize()
                case Event.WINDOW_RESIZE:
                    if not VARIABLES.fullscreen:
                        VARIABLES.set_screen_size(event.data[0], event.data[1])
                        display.refresh_display()
                        renderer.resize()

                case Event.SCREENSHOT:
                    display.screenshot()

                case Event.MOUSE_MOVE:
                    mouse_x = event.data[0] / VARIABLES.screen_width * 1920
                    mouse_y = event.data[1] / VARIABLES.screen_height * 1080
                    # print(mouse_x, mouse_y)

        # Predict
        game.update(events)

        # Send
        client.add_events_to_send([event for event in events if not event.local])

        # Receive
        if client.is_connected():
            received_data = client.get_received_data()
            for state in received_data:
                game.set_state(state)

        # Display
        network_stats = client.get_network_stats()
        renderer.set_network_stats(
            network_stats[0], network_stats[1], network_stats[2], network_stats[3]
        )
        renderer.render(game)

        pygame.display.flip()

    pygame.quit()
    client.disconnect()
    server.stop()
