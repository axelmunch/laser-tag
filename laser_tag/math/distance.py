from math import sqrt

from .Point import Point


def distance(x1, y1, x2, y2) -> float:
    """Returns the distance between two points in 2D space"""
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distance_points(point1: Point, point2: Point) -> float:
    """Returns the distance between two points"""
    return distance(point1.x, point1.y, point2.x, point2.y)
