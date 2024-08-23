import pygame

from ...math.degrees_radians import degrees_to_radians
from ...utils.DeltaTime import DeltaTime
from ..resize import resize
from .Component import Component


class HUD(Component):
    """HUD component"""

    def __init__(self):
        super().__init__()

        self.deactivation_time_ratio = 0
        self.can_attack = True
        self.size_multiplier = 0

        self.set_original_size(250, 250)

        self.update()

    def update(self, deactivation_time_ratio: float = 0, can_attack: bool = True):
        """
        Update the component

        Parameters:
            deactivation_time_ratio (float): Percentage of deactivation time left
            can_attack (bool): Can the player attack
        """

        self.deactivation_time_ratio = min(1, deactivation_time_ratio)
        self.can_attack = can_attack

        if not can_attack:
            self.deactivation_time_ratio = 0.999

        delta_time_value = DeltaTime().get_dt()
        if self.deactivation_time_ratio > 0 and self.deactivation_time_ratio < 1:
            self.size_multiplier = min(1, self.size_multiplier + delta_time_value * 1.5)
        else:
            self.size_multiplier = max(
                0,
                self.size_multiplier * (1 - delta_time_value * 0.5)
                - delta_time_value * 0.5,
            )

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        circle_width = 25
        margin = 50
        radius = (self.original_height / 2 - margin) * self.size_multiplier
        arc_color = (
            255 * (1 if self.deactivation_time_ratio < 1 else self.size_multiplier),
            255
            * ((1 - self.size_multiplier) if self.deactivation_time_ratio == 1 else 0),
            0,
        )

        if radius > 0:
            # Background circle
            pygame.draw.circle(
                self.surface,
                (96, 96, 96, 128),
                (
                    resize(self.original_height / 2, "y"),
                    resize(self.original_height / 2, "y"),
                ),
                resize(radius, "y"),
                int(resize(circle_width, "x")),
            )

            # Arc
            start_angle = degrees_to_radians(90)
            end_angle = degrees_to_radians(
                90 + (1 - self.deactivation_time_ratio + 0.001) * 360
            )

            pygame.draw.arc(
                self.surface,
                arc_color,
                (
                    resize(self.original_height / 2 - radius, "y"),
                    resize(self.original_height / 2 - radius, "y"),
                    resize(radius * 2, "y"),
                    resize(radius * 2, "y"),
                ),
                end_angle,
                start_angle,
                int(resize(circle_width, "x")),
            )

            self.surface.set_alpha(255 * self.size_multiplier)

        super().render()
