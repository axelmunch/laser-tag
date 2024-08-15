from __future__ import annotations

from enum import Enum, auto

from ..math.Line import Line


class WallType(Enum):
    """Wall types"""

    def _generate_next_value_(name, start, count, last_values):
        return start + count

    def __str__(self):
        return str(self.value)

    WALL_1 = auto()
    WALL_2 = auto()
    WALL_3 = auto()
    WALL_4 = auto()


class Wall:
    def __init__(self, wall_type: WallType, line: Line):
        self.type = wall_type
        self.line = line

    def __repr__(self):
        return f"[{self.type},{self.line}]"

    @staticmethod
    def create(parsed_object) -> Wall:
        try:
            wall_type = WallType(parsed_object[0])
            line = Line.create(parsed_object[1])
            if line is None:
                return None
            return Wall(wall_type, line)
        except:
            return None

    def get_line(self) -> Line:
        return self.line

    def get_type(self) -> WallType:
        return self.type
