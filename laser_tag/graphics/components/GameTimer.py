from time import time

from ...configuration import DEFAULT_FONT
from ..resize import resize
from ..Text import Text
from .Component import Component


class GameTimer(Component):
    """Game timer component"""

    def __init__(
        self,
        data={
            "grace_period_seconds": 0,
            "grace_period_end": 0,
            "game_time_seconds": 0,
            "game_time_end": 0,
        },
    ):
        super().__init__()

        self.text = Text(
            DEFAULT_FONT["font"],
            DEFAULT_FONT["font_is_file"],
            DEFAULT_FONT["size_multiplier"],
        )

        self.set_original_size(250, 50)

        self.update(
            data["grace_period_seconds"],
            data["grace_period_end"],
            data["game_time_seconds"],
            data["game_time_end"],
        )

    def update(
        self,
        grace_period_seconds: float,
        grace_period_end: float,
        game_time_seconds: float,
        game_time_end: float,
    ):
        """
        Update the component

        Parameters:
            grace_period_seconds (float): Grace period in seconds
            grace_period_end (float): Grace period end time
            game_time_seconds (float): Game time in seconds
            game_time_end (float): Game end time
        """

        self.data = {
            "grace_period_seconds": grace_period_seconds,
            "grace_period_end": grace_period_end,
            "game_time_seconds": game_time_seconds,
            "game_time_end": game_time_end,
        }
        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        timer_value = 0
        if self.data["game_time_end"] > 0:
            timer_value = self.data["game_time_end"] - min(
                self.data["game_time_end"], time()
            )
        elif self.data["grace_period_end"] > 0:
            timer_value = -(
                self.data["grace_period_end"]
                - min(self.data["grace_period_end"], time())
            )

        if timer_value != 0:
            # Minutes
            text = f"{'-' * (timer_value < 0)}{int(abs(timer_value) / 60) if abs(timer_value) >= 60 else 0:02d}"
            # Seconds
            text += f":{int(abs(timer_value) % 60):02d}"
            if abs(timer_value) < 10:
                # Milliseconds
                text += f":{int((timer_value % 1) * 1000):03d}"

            timer_text = self.text.get_surface(
                text,
                50,
                (255, 255, 255),
            )
            self.surface.blit(
                timer_text,
                (self.width - timer_text.get_width(), resize(0, "y")),
            )

        super().render()
