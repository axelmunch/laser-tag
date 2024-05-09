import pygame
from pygame.locals import *

from laser_tag.configuration import VARIABLES, WINDOW_WINDOWED_SIZE_RATIO
from laser_tag.events.Event import Event
from laser_tag.events.get_events import *
from laser_tag.game.Game import Game
from laser_tag.graphics import display
from laser_tag.graphics.AssetsLoader import load_assets
from laser_tag.graphics.Renderer import Renderer
from laser_tag.graphics.resize import resize
from laser_tag.network.Client import Client
from laser_tag.network.Server import Server

if __name__ == "__main__":
    pygame.init()

    load_assets()

    clock = pygame.time.Clock()

    game = Game()

    renderer = Renderer(clock)

    # Local server
    server = Server(0, debug=False)
    server.start()

    client = Client("localhost", server.get_port(), debug=False)

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
                case Event.GAME_ROTATE:
                    # Center mouse cursor
                    if game.lock_cursor:
                        pygame.mouse.set_pos(resize(960, "x"), resize(540, "y"))

        # Hide or show cursor
        if game.lock_cursor:
            if not pygame.event.get_grab():
                pygame.event.set_grab(True)
                pygame.mouse.set_cursor(
                    pygame.cursors.Cursor(
                        (0, 0), pygame.Surface((1, 1), pygame.SRCALPHA)
                    )
                )
        else:
            if pygame.event.get_grab():
                pygame.event.set_grab(False)
                pygame.mouse.set_cursor(
                    pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
                )

        # Pause menu events
        pause_menu_status = renderer.get_pause_status()
        if pause_menu_status[0]:
            game.game_paused = False
        if pause_menu_status[1]:
            running = False

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
        renderer.set_events(events, game.game_paused)
        renderer.render(game)

        pygame.display.flip()

    pygame.quit()
    client.disconnect()
    server.stop()
