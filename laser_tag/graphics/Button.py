from enum import Enum, auto

from ..language.Language import Language
from ..language.LanguageKey import LanguageKey


class ButtonState(Enum):
    NONE = auto()
    HOVERED = auto()
    PRESSED = auto()
    RELEASED = auto()


class Button:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        text: str = None,
        text_key: LanguageKey = None,
        action=None,
        disabled=False,
    ):
        self.language = Language()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text_str = text
        self.text_key = text_key
        self.action = action

        self.state = ButtonState.NONE

        self.mouse_x = None
        self.mouse_y = None

        self.disabled = disabled

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def is_disabled(self) -> bool:
        return self.disabled

    def get_state(self) -> ButtonState:
        return self.state

    def get_pos(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.width, self.height)

    def get_text(self):
        if self.text_key is not None:
            return self.language.get(self.text_key)
        else:
            return self.text_str

    def update(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        hovered = self.is_hovered()

        if self.state != ButtonState.PRESSED:
            if hovered:
                self.state = ButtonState.HOVERED
            else:
                self.state = ButtonState.NONE

    def is_hovered(self) -> bool:
        if self.mouse_x is None or self.mouse_y is None:
            return False
        return (
            self.mouse_x - self.x >= 0
            and self.mouse_x - self.x <= self.width
            and self.mouse_y - self.y >= 0
            and self.mouse_y - self.y <= self.height
        )

    def click_press(self):
        if self.is_disabled():
            return

        if self.state == ButtonState.HOVERED:
            self.state = ButtonState.PRESSED

    def click_release(self):
        if self.is_disabled():
            return

        if self.state == ButtonState.PRESSED and self.is_hovered():
            self.state = ButtonState.RELEASED
            self.run_action()
        else:
            self.state = ButtonState.NONE

    def run_action(self):
        if self.action is not None:
            return self.action()
