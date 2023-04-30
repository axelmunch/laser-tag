from enum import Enum, auto


class Event(Enum):
    """Events that can be created during the game"""

    def _generate_next_value_(name, start, count, last_values):
        return start + count

    def __str__(self):
        return str(self.value)

    TICK = auto()
    START_GAME = auto()
    MESSAGE = auto()
    TYPE_CHAR = auto()
    GAME_MOVE = auto()
    GAME_MOVE_FORWARD = auto()
    GAME_MOVE_BACKWARD = auto()
    GAME_MOVE_LEFT = auto()
    GAME_MOVE_RIGHT = auto()
    GAME_RUN = auto()
    GAME_JUMP = auto()
    GAME_CROUCH = auto()
    GAME_RELOAD = auto()
    GAME_SHOOT = auto()
    GAME_ROTATE = auto()
    KEY_ESCAPE = auto()
    KEY_ESCAPE_PRESS = auto()
    KEY_RETURN = auto()
    KEY_RETURN_PRESS = auto()
    KEY_TAB = auto()
    KEY_UP = auto()
    KEY_DOWN = auto()
    KEY_LEFT = auto()
    KEY_RIGHT = auto()
    MOUSE_MOVE = auto()
    MOUSE_LEFT_CLICK = auto()
    MOUSE_LEFT_CLICK_PRESS = auto()
    MOUSE_LEFT_CLICK_RELEASE = auto()
    MOUSE_RIGHT_CLICK = auto()
    MOUSE_RIGHT_CLICK_PRESS = auto()
    MOUSE_RIGHT_CLICK_RELEASE = auto()
    MOUSE_MIDDLE_CLICK = auto()
    MOUSE_MIDDLE_CLICK_PRESS = auto()
    MOUSE_MIDDLE_CLICK_RELEASE = auto()
    MOUSE_SCROLL_UP = auto()
    MOUSE_SCROLL_DOWN = auto()
    WINDOW_RESIZE = auto()
    WINDOW_FULLSCREEN = auto()
    WINDOW_QUIT = auto()
    SCREENSHOT = auto()


# Events that are not sent to the server
local_events = [
    Event.MESSAGE,
    Event.TYPE_CHAR,
    Event.GAME_MOVE_FORWARD,
    Event.GAME_MOVE_BACKWARD,
    Event.GAME_MOVE_LEFT,
    Event.GAME_MOVE_RIGHT,
    Event.KEY_ESCAPE,
    Event.KEY_ESCAPE_PRESS,
    Event.KEY_RETURN,
    Event.KEY_RETURN_PRESS,
    Event.KEY_TAB,
    Event.KEY_UP,
    Event.KEY_DOWN,
    Event.KEY_LEFT,
    Event.KEY_RIGHT,
    Event.MOUSE_MOVE,
    Event.MOUSE_LEFT_CLICK,
    Event.MOUSE_LEFT_CLICK_PRESS,
    Event.MOUSE_LEFT_CLICK_RELEASE,
    Event.MOUSE_RIGHT_CLICK,
    Event.MOUSE_RIGHT_CLICK_PRESS,
    Event.MOUSE_RIGHT_CLICK_RELEASE,
    Event.MOUSE_MIDDLE_CLICK,
    Event.MOUSE_MIDDLE_CLICK_PRESS,
    Event.MOUSE_MIDDLE_CLICK_RELEASE,
    Event.MOUSE_SCROLL_UP,
    Event.MOUSE_SCROLL_DOWN,
    Event.WINDOW_RESIZE,
    Event.WINDOW_FULLSCREEN,
    Event.WINDOW_QUIT,
    Event.SCREENSHOT,
]
