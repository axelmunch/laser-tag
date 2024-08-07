from enum import Enum, auto


class Audio(Enum):
    """Audio elements"""

    def __str__(self):
        return str(self.value)

    MENU_1 = auto()


music_audio = [Audio.MENU_1]

loop_audio = [Audio.MENU_1]
