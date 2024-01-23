from enum import Enum, auto


class Item(Enum):
    WALL_1 = auto()
    WALL_2 = auto()
    WALL_3 = auto()
    WALL_4 = auto()
    BARREL_SHORT = auto()
    BARREL_TALL = auto()
    SPAWN_POINT = auto()


wall_items: list[Item] = [
    Item.WALL_1,
    Item.WALL_2,
    Item.WALL_3,
    Item.WALL_4,
]
