import os
from enum import Enum, auto
from subprocess import call
from sys import platform

from ..audio.Audio import Audio
from ..audio.AudioPlayer import AudioPlayer
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

    load_sounds(assets_path)


def load_sounds(path):
    audio_player = AudioPlayer()

    # audio_player.load_sound(Audio.MENU_1, path.joinpath(""))


def load_textures(path):
    textures = Textures()

    textures.load_texture(TextureNames.RED, path.joinpath("red.jpg"), keep=False)
    textures.load_texture(TextureNames.GREEN, path.joinpath("green.jpg"), keep=False)
    textures.load_texture(TextureNames.BLUE, path.joinpath("blue.jpg"), keep=False)
    textures.load_texture(TextureNames.BLACK, path.joinpath("black.jpg"), keep=False)
    textures.load_texture(TextureNames.WHITE, path.joinpath("white.jpg"), keep=False)


def open_assets_folder():
    if platform == "win32":
        os.startfile(ASSETS_PATH)
    else:
        opener = "open" if platform == "darwin" else "xdg-open"
        call([opener, ASSETS_PATH])


def get_assets_folders():
    return [folder.name for folder in ASSETS_PATH.iterdir() if folder.is_dir()]
