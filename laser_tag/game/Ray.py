from ..math.distance import distance_points
from ..math.Point import Point


class Ray:
    """Represents a raycasting ray"""

    def __init__(self, origin: Point, direction: float):
        self.origin = origin
        self.direction = direction

        self.set_hit(origin, hit_infos=None, distance=0)

    def __repr__(self):
        return f"{self.origin}, {self.direction}, {self.hit_point}, {self.hit_infos}, {self.distance}"

    def set_hit(self, hit_point: Point, hit_infos=None, distance=None):
        self.hit_point = hit_point
        self.hit_infos = hit_infos
        if distance is None:
            self.distance = distance_points(self.origin, self.hit_point)
        else:
            self.distance = distance
