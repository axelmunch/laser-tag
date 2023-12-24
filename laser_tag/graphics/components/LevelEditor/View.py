from math import ceil

import pygame

from ....configuration import DEFAULT_FONT
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....math.Line import Line
from ....math.Point import Point
from ....math.rotations import rotate
from ....utils.DeltaTime import DeltaTime
from ...resize import resize
from ...Text import Text
from ..Component import Component


class View(Component):
    """Level editor view component"""

    def __init__(
        self,
        data=[],
    ):
        super().__init__()

        self.text = Text(
            DEFAULT_FONT["font"],
            DEFAULT_FONT["font_is_file"],
            DEFAULT_FONT["size_multiplier"],
        )

        self.set_original_size(1920 - 500, 1080 - 150)

        self.mouse_x = 0
        self.mouse_y = 0

        self.cell_size = 50
        self.max_cell_size = 150
        self.min_cell_size = 30

        self.center_transition_speed = 0.2
        self.center_x_transition = 0
        self.center_y_transition = 0
        self.center_x = 0
        self.center_y = 0

        self.delta_time = DeltaTime()

        self.lines = [
            Line(Point(3, 3), Point(5, 0)),
        ]

        self.scroll_step = 2
        self.move_speed = 0.2

        self.show_grid = True
        self.snap_to_grid = True

        self.reset_center()
        self.update(data)

    def get_lines(self) -> list[Line]:
        return self.lines

    def reset_center(self):
        if len(self.lines) > 0:
            self.center_x_transition = self.lines[0].point1.x
            self.center_y_transition = self.lines[0].point1.y
        else:
            self.center_x_transition = 0
            self.center_y_transition = 0

    def get_point_position(self, point: Point) -> tuple[float, float]:
        return (
            self.original_width / 2 + (point.x - self.center_x) * self.cell_size,
            self.original_height / 2 + (point.y - self.center_y) * self.cell_size,
        )

    def screen_position_to_point(self, x, y) -> Point:
        return Point(
            self.center_x + (x - self.original_width / 2) / self.cell_size,
            self.center_y + (y - self.original_height / 2) / self.cell_size,
        )

    def in_view_screen(self, point: Point) -> bool:
        return (
            point.x >= 0
            and point.x <= self.original_width
            and point.y >= 0
            and point.y <= self.original_height
        )

    def in_view_world(self, point: Point) -> bool:
        return (
            point.x >= self.center_x - self.original_width / 2 / self.cell_size
            and point.x <= self.center_x + self.original_width / 2 / self.cell_size
            and point.y >= self.center_y - self.original_height / 2 / self.cell_size
            and point.y <= self.center_y + self.original_height / 2 / self.cell_size
        )

    def draw_line(self, line: Line, color=(255, 255, 255)):
        pos_point1 = self.get_point_position(line.point1)
        pos_point2 = self.get_point_position(line.point2)
        pygame.draw.line(
            self.surface,
            color,
            (
                resize(pos_point1[0], "x"),
                resize(pos_point1[1], "y"),
            ),
            (
                resize(pos_point2[0], "x"),
                resize(pos_point2[1], "y"),
            ),
            max(1, int(resize(2, "x"))),
        )

    def display_grid(self):
        color = (64, 64, 64)
        middle_x = self.original_width / 2
        middle_y = self.original_height / 2

        for x in range(
            int(-middle_x / self.cell_size), ceil(middle_x / self.cell_size) + 1
        ):
            x_value = (
                x * self.cell_size + middle_x - (self.center_x % 1) * self.cell_size
            )
            pygame.draw.line(
                self.surface,
                color,
                (resize(x_value, "x"), 0),
                (resize(x_value, "x"), self.height),
                max(1, int(resize(2, "x"))),
            )

        for y in range(
            int(-middle_y / self.cell_size), ceil(middle_y / self.cell_size) + 1
        ):
            y_value = (
                y * self.cell_size + middle_y - (self.center_y % 1) * self.cell_size
            )
            pygame.draw.line(
                self.surface,
                color,
                (0, resize(y_value, "y")),
                (self.width, resize(y_value, "y")),
                max(1, int(resize(2, "x"))),
            )

    def update(
        self,
        events: list[EventInstance],
        relative_mouse_position: tuple[int, int] = (0, 0),
    ):
        """
        Update the component

        Parameters:
            events (list): Events
            relative_mouse_position (tuple): Mouse position in the component
        """

        self.data = events
        self.mouse_x = relative_mouse_position[0]
        self.mouse_y = relative_mouse_position[1]

        # Movement transition
        self.center_x += (
            (self.center_x_transition - self.center_x)
            * self.center_transition_speed
            * self.delta_time.get_dt_target()
        )
        self.center_y += (
            (self.center_y_transition - self.center_y)
            * self.center_transition_speed
            * self.delta_time.get_dt_target()
        )

        for event in self.data:
            if event.id == Event.MOUSE_SCROLL_UP:
                self.cell_size = min(
                    self.max_cell_size, self.cell_size + self.scroll_step
                )
            elif event.id == Event.MOUSE_SCROLL_DOWN:
                self.cell_size = max(
                    self.min_cell_size, self.cell_size - self.scroll_step
                )
            elif event.id == Event.MOUSE_LEFT_CLICK_PRESS:
                pass
            elif event.id == Event.MOUSE_MIDDLE_CLICK_PRESS:
                # Reset center
                self.reset_center()
            elif event.id == Event.GAME_MOVE:
                move_vector = rotate(
                    self.move_speed * self.delta_time.get_dt_target(),
                    event.data - 90,
                )
                self.center_x_transition += move_vector.x
                self.center_y_transition += move_vector.y

        super().update()

    def render(self):
        self.surface.fill((42, 42, 42))

        if self.show_grid:
            self.display_grid()

        for line in self.lines:
            self.draw_line(line, (192, 192, 192))
            for point in [line.point1, line.point2]:
                if self.in_view_world(point):
                    pygame.draw.circle(
                        self.surface,
                        (255, 255, 255),
                        (
                            resize(self.get_point_position(point)[0], "x"),
                            resize(self.get_point_position(point)[1], "y"),
                        ),
                        resize(0.1 * self.cell_size, "x"),
                    )

        super().render()
