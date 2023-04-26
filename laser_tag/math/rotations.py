from math import atan2, cos, sin

from .degrees_radians import *
from .Point import Point


def get_angle(point: Point, center=Point(0, 0)) -> float:
    """Returns the angle between the line from the center to the point in degrees (2D space)"""
    x, y = point.x, point.y
    cx, cy = center.x, center.y
    return radians_to_degrees(atan2(y - cy, x - cx)) % 360


def rotate(distance, angle, center=Point(0, 0)) -> Point:
    """Returns a point rotated around a center point by a given angle (degrees) and distance"""
    a = degrees_to_radians(angle)
    return Point(center.x + distance * cos(a), center.y + distance * sin(a))
