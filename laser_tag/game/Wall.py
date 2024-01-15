from ..math.Line import Line


class Wall:
    def __init__(self, line: Line):
        self.line = line

    def get_line(self) -> Line:
        return self.line
