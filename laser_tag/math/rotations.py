from math import atan2, cos, pi, sin, sqrt

from .degrees_radians import *
from .Point import Point


def rotate(distance, angle, center=Point(0, 0)) -> Point:
    a = degrees_to_radians(angle)
    return Point(center.x + distance * cos(a), center.y + distance * sin(a))


def get_angle(point: Point, center=Point(0, 0)):
    x, y = point.x, point.y
    cx, cy = center.x, center.y
    return radians_to_degrees(atan2(y - cy, x - cx)) % 360
