from enum import Enum


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


def get_color(team):
    try:
        team = Team(team)
    except ValueError:
        team = Team.BLACK
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
