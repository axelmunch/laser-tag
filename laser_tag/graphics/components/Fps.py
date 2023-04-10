from ..Text import Text
from .Component import Component


class Fps(Component):
    def __init__(self, data=0):
        super().__init__()

        self.text = Text("calibri")

        self.update(data)

    def update(self, fps):
        """
        Update the component.

        Parameters:
            fps (float): FPS
        """
        self.data = fps
        super().update()

    def render(self):
        self.surface = self.text.get_surface(
            "FPS: " + str(round(self.data, 2)), 40, (255, 255, 255)
        )
