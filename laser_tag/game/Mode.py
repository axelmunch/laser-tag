from enum import Enum, auto

from ..language.LanguageKey import LanguageKey


class Mode(Enum):
    """Game modes"""

    def __str__(self):
        return str(self.value)

    SOLO = auto()
    TEAM = auto()
    SOLO_ELIMINATION = auto()
    TEAM_ELIMINATION = auto()


def get_mode_language_key(mode: Mode | int):
    try:
        mode = Mode(mode)
    except ValueError:
        pass
    match mode:
        case Mode.SOLO:
            return LanguageKey.GAME_MODE_SOLO
        case Mode.TEAM:
            return LanguageKey.GAME_MODE_TEAM
        case Mode.SOLO_ELIMINATION:
            return LanguageKey.GAME_MODE_SOLO_ELIMINATION
        case Mode.TEAM_ELIMINATION:
            return LanguageKey.GAME_MODE_TEAM_ELIMINATION
        case _:
            return LanguageKey.GAME_MODE_SOLO
