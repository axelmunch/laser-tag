from ...configuration import VARIABLES
from ...events.EventInstance import EventInstance
from ...language.LanguageKey import LanguageKey
from .GraphicalElement import GraphicalElement


class GraphicalText(GraphicalElement):
    """Text component"""

    def __init__(
        self,
        x: float,
        y: float,
        align_x: str = "left",
        align_y: str = "top",
        text: str = None,
        text_key: LanguageKey = None,
        size: int = 50,
        color: tuple[int, int, int] = (255, 255, 255),
    ):
        super().__init__()

        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.align_x = align_x
        self.align_y = align_y
        self.text_str = text
        self.text_key = text_key
        self.size = size
        self.color = color

        self.update()

    def get_text_to_render(self):
        if self.text_key is not None:
            return self.language.get(self.text_key)
        else:
            return self.text_str

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        if self.align_x == "center":
            self.x = self.original_x - (self.width * 1920 / VARIABLES.screen_width) / 2
        elif self.align_x == "right":
            self.x = self.original_x - (self.width * 1920 / VARIABLES.screen_width)
        else:
            self.x = self.original_x

        if self.align_y == "center":
            self.y = (
                self.original_y - (self.height * 1080 / VARIABLES.screen_height) / 2
            )
        elif self.align_y == "bottom":
            self.y = self.original_y - (self.height * 1080 / VARIABLES.screen_height)
        else:
            self.y = self.original_y

        super().update()

    def render(self):
        self.surface = self.text.get_surface(
            self.get_text_to_render(), self.size, self.color
        )
        self.width, self.height = self.surface.get_size()

        super().render()
