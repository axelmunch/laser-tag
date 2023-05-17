import pygame

from ..configuration import VARIABLES
from . import display
from .resize import resize


class Text:
    """A class for generating text"""

    def __init__(
        self, font: str, font_is_file: bool = False, size_multiplier: float = 1
    ):
        self.font = font
        self.font_is_file = font_is_file
        self.size_multiplier = size_multiplier
        self.cache = {}

    def create_cache(self, size: float) -> int:
        resized_size = int(resize(size * self.size_multiplier))
        if resized_size not in self.cache:
            if self.font_is_file:
                self.cache[resized_size] = pygame.font.Font(self.font, resized_size)
            else:
                self.cache[resized_size] = pygame.font.SysFont(self.font, resized_size)
        return resized_size

    def clear_cache(self):
        self.cache.clear()

    def generate_text(
        self, text: str, size: int, color=(255, 255, 255)
    ) -> pygame.Surface:
        return self.cache[size].render(str(text), VARIABLES.anti_aliased_text, color)

    def get_size(self, generated_text: pygame.Surface) -> tuple[int, int]:
        return generated_text.get_width(), generated_text.get_height()

    def blit(
        self, generated_text: pygame.Surface, x, y, align_x, align_y
    ) -> tuple[int, int]:
        text_width, text_height = self.get_size(generated_text)

        blit_x, blit_y = resize(x, "x"), resize(y, "y")

        if align_x == "center":
            blit_x -= text_width / 2
        elif align_x == "right":
            blit_x -= text_width

        if align_y == "center":
            blit_y -= text_height / 2
        elif align_y == "bottom":
            blit_y -= text_height

        display.screen.blit(generated_text, (blit_x, blit_y))

        return text_width, text_height

    def text(
        self, text, x, y, size, color=(255, 255, 255), align_x="left", align_y="top"
    ) -> tuple[int, int]:
        return self.blit(self.get_surface(text, size, color), x, y, align_x, align_y)

    def get_surface(self, text, size, color=(255, 255, 255)) -> pygame.Surface:
        resized_size = self.create_cache(size)

        return self.generate_text(text, resized_size, color)
