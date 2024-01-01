from enum import Enum, auto


class EditorState(Enum):
    PLACE = auto()
    MOVE = auto()
    REMOVE = auto()
