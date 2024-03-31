from enum import Enum, auto

from ....game.Wall import WallType


class Item(Enum):
    """Items"""

    def _generate_next_value_(name, start, count, last_values):
        return start + count

    def __str__(self):
        return str(self.value)

    WALL_1 = WallType.WALL_1
    WALL_2 = WallType.WALL_2
    WALL_3 = WallType.WALL_3
    WALL_4 = WallType.WALL_4
    BARREL_SHORT = auto()
    BARREL_TALL = auto()
    SPAWN_POINT = auto()


wall_items: list[Item] = [
    Item.WALL_1,
    Item.WALL_2,
    Item.WALL_3,
    Item.WALL_4,
]
