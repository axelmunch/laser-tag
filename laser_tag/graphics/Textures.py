import pygame

from .Texture import Texture


class Textures:
    """Textures manager"""

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)

            cls.__instance.textures = {}

        return cls.__instance

    def load_texture(
        self,
        name: str,
        path,
        alpha: bool = False,
        custom_size: tuple[int, int] = None,
    ):
        if name not in self.textures:
            self.textures[name] = Texture(path, alpha, custom_size)

    def resize_texture(self, name: str, size: tuple[float, float]) -> pygame.Surface:
        return self.textures[name].resize(size)

    def get_surface(self, name: str) -> pygame.Surface:
        return self.textures[name].get_surface()

    def get_original_size(self, name: str) -> tuple[int, int]:
        return self.textures[name].get_original_size()

    def remove_texture(self, name: str):
        del self.textures[name]

    def clear_cache(self):
        for texture in self.textures.values():
            texture.clear_cache()

    def set_cache_limit(self, name: str, limit: int):
        self.textures[name].set_cache_limit(limit)
