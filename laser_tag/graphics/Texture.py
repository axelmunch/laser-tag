import pygame

from ..configuration import DEFAULT_TEXTURE_CACHE_LIMIT, VARIABLES
from .resize import resize


class Texture:
    """Texture class that manages surfaces and caching"""

    def __init__(self, path, alpha: bool = False, custom_size: tuple[int, int] = None):
        self.texture_cache = {}

        self.cache_limit = DEFAULT_TEXTURE_CACHE_LIMIT

        try:
            texture = pygame.image.load(path)
        except FileNotFoundError:
            if VARIABLES.debug:
                print(f"Texture not found: {path}")
            texture = pygame.Surface((16, 16))
            texture.fill((255, 0, 255))
            pygame.draw.circle(texture, (0, 0, 0), (8, 8), 4)

        if alpha:
            texture = texture.convert_alpha()
        else:
            texture = texture.convert()

        if custom_size:
            texture = pygame.transform.scale(texture, custom_size)

        self.original_width, self.original_height = texture.get_size()

        self.texture_original = texture

        self.resize()

    def resize(self, size: tuple[float, float] = None) -> pygame.Surface:
        if size is None:
            size = (self.original_width, self.original_height)

        size = (int(resize(size[0], "x")), int(resize(size[1], "y")))

        if size not in self.texture_cache:
            self.texture_cache[size] = pygame.transform.scale(
                self.texture_original, size
            )

            self.reduce_cache()

        return self.texture_cache[size]

    def get_surface(self) -> pygame.Surface:
        return self.resize()

    def get_original_surface(self) -> pygame.Surface:
        return self.texture_original

    def get_original_size(self) -> tuple[int, int]:
        return self.original_width, self.original_height

    def reduce_cache(self):
        if len(self.texture_cache) > self.cache_limit:
            self.texture_cache = dict(
                list(self.texture_cache.items())[-self.cache_limit :]
            )

    def clear_cache(self):
        self.texture_cache.clear()

    def set_cache_limit(self, limit: int):
        self.cache_limit = limit
        self.reduce_cache()
