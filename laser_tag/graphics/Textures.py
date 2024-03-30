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
        id,
        path,
        alpha: bool = False,
        custom_size: tuple[int, int] = None,
        keep: bool = True,
    ):
        if id not in self.textures or not keep:
            self.textures[id] = Texture(path, alpha, custom_size)

    def resize_texture(self, id, size: tuple[float, float]) -> pygame.Surface:
        return self.textures[id].resize(size)

    def get_surface(self, id) -> pygame.Surface:
        return self.textures[id].get_surface()

    def get_original_size(self, id) -> tuple[int, int]:
        return self.textures[id].get_original_size()

    def remove_texture(self, id):
        del self.textures[id]

    def clear_cache(self):
        for texture in self.textures.values():
            texture.clear_cache()

    def set_cache_limit(self, id, limit: int):
        self.textures[id].set_cache_limit(limit)
