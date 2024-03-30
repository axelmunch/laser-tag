from enum import Enum, auto

from ..configuration import ASSETS_PATH, VARIABLES
from .Textures import Textures


class TextureNames(Enum):
    """Texture names"""

    def _generate_next_value_(name, start, count, last_values):
        return start + count

    def __str__(self):
        return str(self.value)

    RED = auto()
    GREEN = auto()
    BLUE = auto()
    BLACK = auto()
    WHITE = auto()


def load_assets():
    assets_path = ASSETS_PATH.joinpath(VARIABLES.assets_folder)

    load_textures(assets_path)


def load_textures(path):
    textures = Textures()

    textures.load_texture(TextureNames.RED, path.joinpath("red.jpg"), keep=False)
    textures.load_texture(TextureNames.GREEN, path.joinpath("green.jpg"), keep=False)
    textures.load_texture(TextureNames.BLUE, path.joinpath("blue.jpg"), keep=False)
    textures.load_texture(TextureNames.BLACK, path.joinpath("black.jpg"), keep=False)
    textures.load_texture(TextureNames.WHITE, path.joinpath("white.jpg"), keep=False)
