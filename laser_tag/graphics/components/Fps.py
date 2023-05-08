from ...configuration import DEFAULT_FONT
from ..Text import Text
from .Component import Component


class Fps(Component):
    """FPS component"""

    def __init__(self, data=0):
        super().__init__()

        self.text = Text(
            DEFAULT_FONT["font"],
            DEFAULT_FONT["font_is_file"],
            DEFAULT_FONT["size_multiplier"],
        )

        self.update(data)

    def update(self, fps: float):
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

        super().render()
