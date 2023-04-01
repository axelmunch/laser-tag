from .Point import Point


class Box:
    def __init__(self, origin: Point, length, width, height=None):
        self.origin = origin
        self.length = length
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Box({self.origin}, {self.length}, {self.width}, {self.height})"
