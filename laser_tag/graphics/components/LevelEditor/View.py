from math import ceil

import pygame

from ....configuration import DEFAULT_FONT
from ....entities.Player import Player
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....math.distance import distance_points
from ....math.Line import Line
from ....math.Point import Point
from ....math.rotations import rotate
from ....utils.DeltaTime import DeltaTime
from ...resize import resize
from ...Text import Text
from ..Component import Component
from .EditorState import EditorState
from .Item import Item


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
        self.min_cell_size = 25

        self.center_transition_speed = 0.2
        self.center_x_transition = 0
        self.center_y_transition = 0
        self.center_x = 0
        self.center_y = 0

        self.delta_time = DeltaTime()

        self.lines = [
            Line(Point(3, 3), Point(5, 0)),
        ]

        self.scroll_step = 4
        self.move_speed = 0.2

        self.preview_radius = Player.entity_radius()

        self.snap_to_grid = True
        self.show_grid = True
        self.preview_player = False

        self.editor_state = EditorState.PLACE
        self.selected_item = None

        self.position_aimed = Point(0, 0)

        self.min_selection_distance = 0.25
        self.placing_or_moving = False
        self.selected_elements = []

        self.reset_center()
        self.update(data)

    def set_editor_state(self, editor_state: EditorState):
        if editor_state != self.editor_state:
            self.cancel_placing_or_moving()
        self.editor_state = editor_state

    def set_selected_item(self, item: Item):
        if item != self.selected_item:
            self.cancel_placing_or_moving()
        self.selected_item = item

    def set_view_variables(
        self, snap_to_grid: bool, show_grid: bool, preview_player: bool
    ):
        self.snap_to_grid = snap_to_grid
        self.show_grid = show_grid
        self.preview_player = preview_player

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

    def snap_coordinates(self, point: Point) -> Point:
        # Only allow 0, 0.5 and 1 coordinates in the cell
        return Point(
            round(point.x * 2) / 2,
            round(point.y * 2) / 2,
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
            max(1, int(resize(3, "x"))),
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

    def manage_click(
        self,
        mouse_left_click_press: bool,
        mouse_left_click_release: bool,
        mouse_right_click_press: bool,
    ):
        # Place or move an element

        if not self.in_view_screen(Point(self.mouse_x, self.mouse_y)):
            return

        if mouse_right_click_press and not self.placing_or_moving:
            # Remove
            nearest_element_position = self.find_nearest_object_position(
                self.screen_position_to_point(self.mouse_x, self.mouse_y)
            )
            if nearest_element_position is not None:
                self.delete_element_containing_point(nearest_element_position)

        match self.editor_state:
            case EditorState.PLACE:
                if mouse_left_click_press and not self.placing_or_moving:
                    self.placing_or_moving = True
                    self.selected_elements.append(self.position_aimed)
                elif mouse_left_click_release and self.placing_or_moving:
                    if len(self.selected_elements) > 0:
                        if (
                            type(self.selected_elements[-1]) == Point
                            and self.selected_elements[-1] != self.position_aimed
                        ):
                            self.lines.append(
                                Line(self.selected_elements[-1], self.position_aimed)
                            )
                        self.selected_elements = []
                    self.placing_or_moving = False
                if mouse_right_click_press and self.placing_or_moving:
                    # Cancel place
                    self.cancel_placing_or_moving()
            case EditorState.MOVE:
                if mouse_left_click_press and not self.placing_or_moving:
                    # Find nearest element
                    nearest_element_position = self.find_nearest_object_position(
                        self.screen_position_to_point(self.mouse_x, self.mouse_y)
                    )
                    if nearest_element_position is not None:
                        self.placing_or_moving = True
                        # Add to selected
                        # Copy of original at [0], reference to current at [1]
                        self.selected_elements.append(
                            Point(
                                nearest_element_position.x, nearest_element_position.y
                            )
                        )
                        self.selected_elements.append(nearest_element_position)

                elif mouse_left_click_release and self.placing_or_moving:
                    # Complete move
                    self.placing_or_moving = False
                    self.selected_elements = []

                if mouse_right_click_press and self.placing_or_moving:
                    # Cancel move
                    self.cancel_placing_or_moving()

                if self.placing_or_moving:
                    # Move point
                    if (
                        len(self.selected_elements) > 0
                        and type(self.selected_elements[-1]) == Point
                    ):
                        self.selected_elements[-1].x = self.position_aimed.x
                        self.selected_elements[-1].y = self.position_aimed.y

    def find_nearest_object_position(self, point: Point) -> Point | None:
        # [(point, distance)]
        objects_distance = []

        for line in self.lines:
            for line_point in [line.point1, line.point2]:
                distance = distance_points(point, line_point)
                if distance <= self.min_selection_distance:
                    objects_distance.append((line_point, distance))

        # Sort by distance
        objects_distance.sort(key=lambda element: element[1])

        if len(objects_distance) > 0:
            return objects_distance[0][0]

        return None

    def delete_element_containing_point(self, point: Point):
        for line in self.lines:
            if line.point1 == point or line.point2 == point:
                self.lines.remove(line)
                return

    def cancel_placing_or_moving(self):
        match self.editor_state:
            case EditorState.PLACE:
                pass
            case EditorState.MOVE:
                if (
                    len(self.selected_elements) > 1
                    and type(self.selected_elements[-1]) == Point
                    and type(self.selected_elements[-2]) == Point
                ):
                    # Reset coordinates
                    self.selected_elements[-1].x = self.selected_elements[-2].x
                    self.selected_elements[-1].y = self.selected_elements[-2].y

        self.placing_or_moving = False
        self.selected_elements = []

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

        self.position_aimed = self.screen_position_to_point(self.mouse_x, self.mouse_y)
        if self.snap_to_grid:
            self.position_aimed = self.snap_coordinates(self.position_aimed)

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

        mouse_left_click_press = False
        mouse_left_click_release = False
        mouse_right_click_press = False

        for event in self.data:
            if event.id == Event.MOUSE_LEFT_CLICK_PRESS:
                mouse_left_click_press = True
            elif event.id == Event.MOUSE_LEFT_CLICK_RELEASE:
                mouse_left_click_release = True
            elif event.id == Event.MOUSE_RIGHT_CLICK_PRESS:
                mouse_right_click_press = True
            elif event.id == Event.MOUSE_MIDDLE_CLICK_PRESS:
                # Reset center
                self.reset_center()
            elif event.id == Event.MOUSE_SCROLL_UP:
                if self.in_view_screen(Point(self.mouse_x, self.mouse_y)):
                    self.cell_size = min(
                        self.max_cell_size, self.cell_size + self.scroll_step
                    )
            elif event.id == Event.MOUSE_SCROLL_DOWN:
                if self.in_view_screen(Point(self.mouse_x, self.mouse_y)):
                    self.cell_size = max(
                        self.min_cell_size, self.cell_size - self.scroll_step
                    )
            elif event.id == Event.GAME_MOVE:
                move_vector = rotate(
                    self.move_speed * self.delta_time.get_dt_target(),
                    event.data - 90,
                )
                self.center_x_transition += move_vector.x
                self.center_y_transition += move_vector.y

        self.manage_click(
            mouse_left_click_press, mouse_left_click_release, mouse_right_click_press
        )

        super().update()

    def render(self):
        self.surface.fill((42, 42, 42))

        if self.preview_player:
            pygame.draw.circle(
                self.surface,
                (64, 64, 128),
                (
                    resize(self.mouse_x, "x"),
                    resize(self.mouse_y, "y"),
                ),
                resize(self.preview_radius * self.cell_size, "x"),
            )

        if self.show_grid:
            self.display_grid()

        # Aimed point indicator
        point = self.get_point_position(self.position_aimed)
        pygame.draw.circle(
            self.surface,
            (128, 128, 128),
            (
                resize(point[0], "x"),
                resize(point[1], "y"),
            ),
            resize(0.2 * self.cell_size, "x"),
            max(1, int(resize(2, "x"))),
        )
        pygame.draw.circle(
            self.surface,
            (128, 128, 128),
            (
                resize(point[0], "x"),
                resize(point[1], "y"),
            ),
            max(1, int(resize(2, "x"))),
        )

        # Draw all lines
        for line in self.lines:
            self.draw_line(line, (192, 192, 192))
            for point in [line.point1, line.point2]:
                if self.in_view_world(point):
                    point_position = self.get_point_position(point)
                    pygame.draw.circle(
                        self.surface,
                        (255, 255, 255),
                        (
                            resize(point_position[0], "x"),
                            resize(point_position[1], "y"),
                        ),
                        resize(0.1 * self.cell_size, "x"),
                    )

        # Preview line creation
        if self.editor_state == EditorState.PLACE:
            if (
                len(self.selected_elements) > 0
                and type(self.selected_elements[-1]) == Point
            ):
                color = (128, 128, 128)

                self.draw_line(
                    Line(self.selected_elements[-1], self.position_aimed),
                    color,
                )

                point_position = self.get_point_position(self.position_aimed)
                pygame.draw.circle(
                    self.surface,
                    color,
                    (
                        resize(point_position[0], "x"),
                        resize(point_position[1], "y"),
                    ),
                    resize(0.1 * self.cell_size, "x"),
                )

        # Proximity indicator
        if not self.placing_or_moving:
            nearest_element_position = self.find_nearest_object_position(
                self.screen_position_to_point(self.mouse_x, self.mouse_y)
            )
            if nearest_element_position is not None:
                point_position = self.get_point_position(nearest_element_position)
                pygame.draw.circle(
                    self.surface,
                    (192, 128, 192),
                    (
                        resize(point_position[0], "x"),
                        resize(point_position[1], "y"),
                    ),
                    resize(0.2 * self.cell_size, "x"),
                    max(1, int(resize(2, "x"))),
                )

        super().render()
