from math import sqrt

from .Point import Point


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distance_3d(x1, y1, z1, x2, y2, z2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def distance_points(point1: Point, point2: Point):
    if point1.z is not None and point2.z is not None:
        return distance_3d(point1.x, point1.y, point1.z, point2.x, point2.y, point2.z)
    return distance(point1.x, point1.y, point2.x, point2.y)
