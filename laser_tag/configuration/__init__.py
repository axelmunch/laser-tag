from pathlib import Path

from .variables import *

VERSION = "v0.0.8"
GAME_NAME = "Laser Tag"

WINDOW_WINDOWED_SIZE_RATIO = 0.5

TARGET_FPS = 60

DEFAULT_FONT = {"font": "calibri", "font_is_file": False, "size_multiplier": 1}

# Paths
DATA_PATH = Path("data")
ASSETS_PATH = DATA_PATH.joinpath("assets")
SETTINGS_FILE = DATA_PATH.joinpath("settings.json")

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
DEFAULT_TEXTURE_CACHE_LIMIT = 200
MAX_WALL_HEIGHT = 2500
MAX_RAY_DISTANCE = 50


VARIABLES = Variables(SETTINGS_FILE)
