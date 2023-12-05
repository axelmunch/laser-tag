from enum import Enum, auto


class Mode(Enum):
    """Game modes"""

    def __str__(self):
        return str(self.value)

    SOLO = auto()
    TEAM = auto()
    SOLO_ELIMINATION = auto()
    TEAM_ELIMINATION = auto()
