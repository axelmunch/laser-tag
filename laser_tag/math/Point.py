class Point:
    """A point is represented by three positions: x, y and z. If z is not defined, the point is 2D"""

    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"
