from ..configuration import VARIABLES


def resize(size_1080p, x_y):
    if x_y == "x":
        return size_1080p * VARIABLES.screen_width / 1920
    return size_1080p * VARIABLES.screen_height / 1080
