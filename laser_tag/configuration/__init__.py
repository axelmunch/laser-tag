from pathlib import Path

from .variables import *

VERSION = "v0.0.12"
GAME_NAME = "Laser Tag"

TARGET_FPS = 60

DEFAULT_FONT = {"font": "calibri", "font_is_file": False, "size_multiplier": 1}

# Paths
DATA_PATH = Path("data")
ASSETS_PATH = DATA_PATH.joinpath("assets")
SETTINGS_FILE = DATA_PATH.joinpath("settings.json")
LANGUAGE_FILE = DATA_PATH.joinpath("language.json")
WORLDS_PATH = DATA_PATH.joinpath("worlds")
GAME_WORLD_FILE = WORLDS_PATH.joinpath("game_world.json")
LEVEL_EDITOR_WORLD_FILE = WORLDS_PATH.joinpath("level_editor_world.json")

SCREENSHOTS_PATH = Path("screenshots")

# Networking
NETWORK_BUFFER_SIZE = 32768
SERVER_DEFAULT_MAX_CLIENTS = None
SERVER_DELTA_TIME_NAME = "SERVER"
SERVER_TIMEOUT = 10
SERVER_SOCKET_TIMEOUT = 2
CLIENT_TIMEOUT = 5
CLIENT_MINIMUM_TICK = 30

# Performance
DEFAULT_TEXTURE_CACHE_LIMIT = 128
MAX_WALL_HEIGHT = 2500
MAX_RAY_DISTANCE = 50

MAX_PLAYER_NAME_LENGTH = 16


VARIABLES = Variables(VERSION, SETTINGS_FILE)
