from enum import Enum

from ..language.LanguageKey import LanguageKey


class Team(Enum):
    """Teams"""

    def __str__(self):
        return str(self.value)

    NONE = -1
    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3
    ORANGE = 4
    PINK = 5
    BLACK = 6
    WHITE = 7


def get_team_language_key(team: Team | int):
    try:
        team = Team(team)
    except ValueError:
        team = Team.NONE
    match team:
        case Team.NONE:
            return LanguageKey.TEAM_ALL
        case Team.RED:
            return LanguageKey.TEAM_RED
        case Team.BLUE:
            return LanguageKey.TEAM_BLUE
        case Team.GREEN:
            return LanguageKey.TEAM_GREEN
        case Team.YELLOW:
            return LanguageKey.TEAM_YELLOW
        case Team.ORANGE:
            return LanguageKey.TEAM_ORANGE
        case Team.PINK:
            return LanguageKey.TEAM_PINK
        case Team.BLACK:
            return LanguageKey.TEAM_BLACK
        case Team.WHITE:
            return LanguageKey.TEAM_WHITE
        case _:
            return LanguageKey.TEAM_ALL


def get_team_color(team: Team | int):
    try:
        team = Team(team)
    except ValueError:
        team = Team.NONE
    match team:
        case Team.NONE:
            return (255, 0, 0)
        case Team.RED:
            return (255, 0, 0)
        case Team.BLUE:
            return (0, 0, 255)
        case Team.GREEN:
            return (0, 255, 0)
        case Team.YELLOW:
            return (255, 255, 0)
        case Team.ORANGE:
            return (255, 128, 0)
        case Team.PINK:
            return (255, 0, 255)
        case Team.BLACK:
            return (0, 0, 0)
        case Team.WHITE:
            return (255, 255, 255)
