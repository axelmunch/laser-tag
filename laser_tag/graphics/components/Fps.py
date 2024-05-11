from ...language.LanguageKey import LanguageKey
from .Component import Component


class Fps(Component):
    """FPS component"""

    def __init__(self, data=0):
        super().__init__()

        self.update(data)

    def update(self, fps: float):
        """
        Update the component

        Parameters:
            fps (float): FPS
        """
        self.data = fps
        super().update()

    def render(self):
        self.surface = self.text.get_surface(
            self.language.get(LanguageKey.GAME_FPS) + " " + str(round(self.data, 2)),
            40,
            (255, 255, 255),
        )
        self.width, self.height = self.surface.get_size()

        super().render()
