from enum import Enum, auto


class LanguageKey(Enum):
    """Keys to access language content"""

    def _generate_next_value_(name, start, count, last_values):
        return start + count

    def __str__(self):
        return str(self.name)

    GAME_NAME = auto()

    NETWORK_STATS_CONNECTED = auto()
    NETWORK_STATS_DISCONNECTED = auto()
    NETWORK_STATS_CONNECTING = auto()
    NETWORK_STATS_PING = auto()
    NETWORK_STATS_AVG_SEND_TICK = auto()
    NETWORK_STATS_SEND_SECOND = auto()
    NETWORK_STATS_AVG_SEND = auto()
    NETWORK_STATS_MAX_SEND = auto()
    NETWORK_STATS_AVG_RECV = auto()
    NETWORK_STATS_MAX_RECV = auto()
    NETWORK_STATS_KBITS_UNIT = auto()

    LEVEL_EDITOR_QUIT = auto()
    LEVEL_EDITOR_SAVE = auto()
    LEVEL_EDITOR_LOAD = auto()
    LEVEL_EDITOR_PLACE = auto()
    LEVEL_EDITOR_MOVE = auto()
    LEVEL_EDITOR_SNAP = auto()
    LEVEL_EDITOR_GRID = auto()
    LEVEL_EDITOR_PREVIEW = auto()
    LEVEL_EDITOR_HELP = auto()
    LEVEL_EDITOR_ITEM_WALL_1 = auto()
    LEVEL_EDITOR_ITEM_WALL_2 = auto()
    LEVEL_EDITOR_ITEM_WALL_3 = auto()
    LEVEL_EDITOR_ITEM_WALL_4 = auto()
    LEVEL_EDITOR_ITEM_BARREL_SHORT = auto()
    LEVEL_EDITOR_ITEM_BARREL_TALL = auto()
    LEVEL_EDITOR_ITEM_SPAWN_POINT = auto()

    GAME_FPS = auto()
    GAME_SCOREBOARD_TITLE = auto()
    GAME_SCOREBOARD_TEAM = auto()
    GAME_SCOREBOARD_NAME = auto()
    GAME_SCOREBOARD_SCORE = auto()
    GAME_SCOREBOARD_ELIMINATIONS = auto()
    GAME_SCOREBOARD_DEATHS = auto()

    MENU_MAIN_PLAY = auto()
    MENU_MAIN_SETTINGS = auto()
    MENU_MAIN_QUIT = auto()

    MENU_PAUSE_TITLE = auto()
    MENU_PAUSE_INFORMATION = auto()
    MENU_PAUSE_RESUME = auto()
    MENU_PAUSE_SETTINGS = auto()
    MENU_PAUSE_QUIT = auto()

    MENU_CONFIRMATION_YES = auto()
    MENU_CONFIRMATION_NO = auto()
    MENU_CONFIRMATION_QUIT_GAME = auto()
    MENU_CONFIRMATION_CLOSE_GAME = auto()

    MENU_SETTINGS_TITLE = auto()
    MENU_SETTINGS_BACK = auto()
