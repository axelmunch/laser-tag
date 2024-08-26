import pygame
from pygame.locals import *

from .Event import Event
from .EventInstance import EventInstance


def get_events() -> list[EventInstance]:
    """Returns a list of EventInstance objects"""
    events = []

    # Unique events
    events.append(EventInstance(Event.TICK))
    for event in pygame.event.get():
        if event.type == QUIT:
            events.append(EventInstance(Event.WINDOW_QUIT))
        elif event.type == KEYDOWN:
            if event.unicode.isprintable() and len(event.unicode) > 0:
                events.append(EventInstance(Event.TYPE_CHAR, event.unicode[0]))

            if event.key == K_ESCAPE:
                events.append(EventInstance(Event.KEY_ESCAPE_PRESS))
            elif event.key == K_RETURN or event.key == K_KP_ENTER:
                events.append(EventInstance(Event.KEY_RETURN_PRESS))
                events.append(EventInstance(Event.START_GAME))
            elif event.key == K_BACKSPACE:
                events.append(EventInstance(Event.KEY_BACKSPACE_PRESS))
            elif event.key == K_F11:
                events.append(EventInstance(Event.WINDOW_FULLSCREEN))
            elif event.key == K_F12:
                events.append(EventInstance(Event.SCREENSHOT))
        elif event.type == pygame.VIDEORESIZE:
            events.append(EventInstance(Event.WINDOW_RESIZE, [event.w, event.h]))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                events.append(EventInstance(Event.MOUSE_LEFT_CLICK_PRESS))
            elif event.button == 2:
                events.append(EventInstance(Event.MOUSE_MIDDLE_CLICK_PRESS))
            elif event.button == 3:
                events.append(EventInstance(Event.MOUSE_RIGHT_CLICK_PRESS))

            elif event.button == 4:
                events.append(EventInstance(Event.MOUSE_SCROLL_UP))
            elif event.button == 5:
                events.append(EventInstance(Event.MOUSE_SCROLL_DOWN))

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                events.append(EventInstance(Event.MOUSE_LEFT_CLICK_RELEASE))
            elif event.button == 2:
                events.append(EventInstance(Event.MOUSE_MIDDLE_CLICK_RELEASE))
            elif event.button == 3:
                events.append(EventInstance(Event.MOUSE_RIGHT_CLICK_RELEASE))

        elif event.type == pygame.MOUSEMOTION:
            events.append(EventInstance(Event.MOUSE_MOVE, [event.pos[0], event.pos[1]]))

    key_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()

    # Game events
    if key_pressed[K_w]:
        events.append(EventInstance(Event.GAME_MOVE_FORWARD))
    if key_pressed[K_s]:
        events.append(EventInstance(Event.GAME_MOVE_BACKWARD))
    if key_pressed[K_a]:
        events.append(EventInstance(Event.GAME_MOVE_LEFT))
    if key_pressed[K_d]:
        events.append(EventInstance(Event.GAME_MOVE_RIGHT))
    if key_pressed[K_LSHIFT]:
        events.append(EventInstance(Event.GAME_RUN))
    if key_pressed[K_SPACE]:
        events.append(EventInstance(Event.GAME_JUMP))
    if key_pressed[K_LCTRL]:
        events.append(EventInstance(Event.GAME_CROUCH))
    if key_pressed[K_r]:
        events.append(EventInstance(Event.GAME_RELOAD))

    # Key events
    if key_pressed[K_ESCAPE]:
        events.append(EventInstance(Event.KEY_ESCAPE))
    if key_pressed[K_RETURN] or key_pressed[K_KP_ENTER]:
        events.append(EventInstance(Event.KEY_RETURN))
    if key_pressed[K_BACKSPACE]:
        events.append(EventInstance(Event.KEY_BACKSPACE))
    if key_pressed[K_TAB]:
        events.append(EventInstance(Event.KEY_TAB))
        events.append(EventInstance(Event.GAME_SCOREBOARD))

    if key_pressed[K_UP]:
        events.append(EventInstance(Event.KEY_UP))
    if key_pressed[K_DOWN]:
        events.append(EventInstance(Event.KEY_DOWN))
    if key_pressed[K_LEFT]:
        events.append(EventInstance(Event.KEY_LEFT))
    if key_pressed[K_RIGHT]:
        events.append(EventInstance(Event.KEY_RIGHT))

    # Mouse events
    if mouse_buttons[0]:
        events.append(EventInstance(Event.MOUSE_LEFT_CLICK))
        events.append(EventInstance(Event.GAME_SHOOT))
    if mouse_buttons[1]:
        events.append(EventInstance(Event.MOUSE_MIDDLE_CLICK))
    if mouse_buttons[2]:
        events.append(EventInstance(Event.MOUSE_RIGHT_CLICK))

    return events
