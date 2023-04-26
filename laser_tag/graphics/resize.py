from ..configuration import VARIABLES


def resize(size_1080p: float, x_y="y") -> float:
    if x_y == "x":
        return size_1080p * VARIABLES.screen_width / 1920
    return size_1080p * VARIABLES.screen_height / 1080
