import pygame
from pygame.locals import *

from ..configuration import VARIABLES
from .Event import Event
from .EventInstance import EventInstance

number_events = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]
keypad_events = [K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]


def get_events() -> list[EventInstance]:
    """Returns a list of EventInstance objects"""
    events = []

    # Unique events
    events.append(EventInstance(Event.TICK))
    for event in pygame.event.get():
        if event.type == QUIT:
            events.append(EventInstance(Event.WINDOW_QUIT))
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                events.append(EventInstance(Event.KEY_ESCAPE_PRESS))
            elif event.key == K_RETURN:
                events.append(EventInstance(Event.KEY_RETURN_PRESS))
                events.append(EventInstance(Event.START_GAME))
            elif event.key == K_F11:
                events.append(EventInstance(Event.WINDOW_FULLSCREEN))
            elif event.key == K_F12:
                events.append(EventInstance(Event.SCREENSHOT))
            elif event.key in number_events:
                events.append(
                    EventInstance(
                        Event.GAME_SELECT_TEAM, number_events.index(event.key) - 1
                    )
                )
            elif event.key in keypad_events:
                events.append(
                    EventInstance(
                        Event.GAME_SELECT_TEAM, keypad_events.index(event.key) - 1
                    )
                )
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
    if key_pressed[K_RETURN]:
        events.append(EventInstance(Event.KEY_RETURN))
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
