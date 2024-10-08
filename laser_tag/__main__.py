import pygame
from pygame.locals import *

from laser_tag.audio.AudioManager import AudioManager
from laser_tag.audio.AudioPlayer import AudioPlayer
from laser_tag.configuration import VARIABLES
from laser_tag.events.Event import Event
from laser_tag.events.get_events import *
from laser_tag.game.Game import Game
from laser_tag.graphics import display
from laser_tag.graphics.AssetsLoader import load_assets
from laser_tag.graphics.components.menus.Menus import Menus
from laser_tag.graphics.Renderer import Renderer
from laser_tag.graphics.resize import resize
from laser_tag.network.ClientServerGroup import ClientServerGroup

if __name__ == "__main__":
    pygame.init()

    load_assets()

    clock = pygame.time.Clock()

    game = Game(server_mode=False)

    menus = Menus()

    renderer = Renderer(clock)

    audio_manager = AudioManager()
    audio_manager.set_audio_player(AudioPlayer())

    # Main menu
    game.game_paused = True
    renderer.open_main_menu(game)

    client_server = ClientServerGroup()

    running = True

    while running:
        clock.tick(VARIABLES.fps)

        # Events
        events = get_events()
        server_events = menus.get_events()

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
                    VARIABLES.resize_display = True
                case Event.WINDOW_RESIZE:
                    if not VARIABLES.fullscreen:
                        VARIABLES.set_screen_size(event.data[0], event.data[1])
                        display.refresh_display(free_aspect_ratio=True)
                        renderer.resize()
                case Event.SCREENSHOT:
                    display.screenshot()
                case Event.GAME_ROTATE:
                    # Center mouse cursor
                    if game.lock_cursor:
                        pygame.mouse.set_pos(resize(960, "x"), resize(540, "y"))

        if VARIABLES.resize_display:
            display.refresh_display()
            renderer.resize()
            VARIABLES.resize_display = False

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

        if client_server.is_client_connected():
            # Send
            client_server.get_client().add_events_to_send(
                [
                    event
                    for event in events + server_events
                    if not event.local and not (game.game_paused and event.game)
                ]
            )

            # Receive
            if client_server.is_client_connected():
                received_data = client_server.get_client().get_received_data()
                for state in received_data:
                    game.set_state(state)

        if client_server.get_client() is not None:
            # Display
            if VARIABLES.show_network_stats:
                network_stats = client_server.get_client().get_network_stats()
                renderer.set_network_stats(
                    network_stats[0],
                    network_stats[1],
                    network_stats[2],
                    network_stats[3],
                )

        # Predict
        game.update(events)

        current_position = game.world.get_current_position()
        if current_position is not None:
            audio_manager.set_listening_position(current_position)
        audio_manager.update(events)

        renderer.update(game, events)

        # Close game event from menus
        if renderer.close_game_event():
            running = False

        renderer.render(game)

        pygame.display.flip()

    pygame.quit()
    client_server.disconnect_client()
    client_server.stop_server()
