from math import ceil

import pygame

from ....configuration import DEFAULT_FONT
from ....entities.BarrelShort import BarrelShort
from ....entities.BarrelTall import BarrelTall
from ....entities.GameEntity import GameEntity
from ....entities.Player import Player
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....game.Wall import Wall
from ....math.distance import distance_points
from ....math.Line import Line
from ....math.Point import Point
from ....math.rotations import rotate
from ....utils.DeltaTime import DeltaTime
from ...resize import resize
from ...Text import Text
from ..Component import Component
from .EditorState import EditorState
from .Item import Item, wall_items


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

        self.walls = []
        self.entities: list[GameEntity] = []
        self.spawn_points: list[Point] = []

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
        self.selected_elements: list[Point] = []

        self.reset_center()
        self.update(data)

    def get_map_data(self):
        return {
            "walls": self.get_walls(),
            "entities": self.entities,
            "spawn_points": self.spawn_points,
        }

    def set_map_data(self, map_data: dict):
        self.walls = map_data["walls"]
        self.entities = map_data["entities"]
        self.spawn_points = map_data["spawn_points"]

        self.reset_center()

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

    def get_walls(self) -> list[Wall]:
        return self.walls

    def reset_center(self):
        if len(self.walls) > 0:
            self.center_x_transition = self.walls[0].get_line().point1.x
            self.center_y_transition = self.walls[0].get_line().point1.y
        elif len(self.entities) > 0:
            self.center_x_transition = self.entities[0].position.x
            self.center_y_transition = self.entities[0].position.y
        elif len(self.spawn_points) > 0:
            self.center_x_transition = self.spawn_points[0].x
            self.center_y_transition = self.spawn_points[0].y
        else:
            self.center_x_transition = 0
            self.center_y_transition = 0

    def screen_position_to_world_point(self, x: float, y: float) -> Point:
        return Point(
            self.center_x + (x - self.original_width / 2) / self.cell_size,
            self.center_y + (y - self.original_height / 2) / self.cell_size,
        )

    def world_point_to_screen_position(self, point: Point) -> tuple[float, float]:
        return (
            self.original_width / 2 + (point.x - self.center_x) * self.cell_size,
            self.original_height / 2 + (point.y - self.center_y) * self.cell_size,
        )

    def in_view_screen(self, x: float, y: float) -> bool:
        return (
            x >= 0 and x <= self.original_width and y >= 0 and y <= self.original_height
        )

    def in_view_world(self, point: Point) -> bool:
        return (
            point.x >= self.center_x - self.original_width / 2 / self.cell_size
            and point.x <= self.center_x + self.original_width / 2 / self.cell_size
            and point.y >= self.center_y - self.original_height / 2 / self.cell_size
            and point.y <= self.center_y + self.original_height / 2 / self.cell_size
        )

    def in_view_world_rect(self, rect: tuple[float, float, float, float]) -> bool:
        start = self.screen_position_to_world_point(0, 0)
        end = self.screen_position_to_world_point(
            self.original_width, self.original_height
        )

        editor_visibility_zone = (start.x, start.y, end.x - start.x, end.y - start.y)

        return (
            rect[0] <= editor_visibility_zone[0] + editor_visibility_zone[2]
            and rect[0] + rect[2] >= editor_visibility_zone[0]
            and rect[1] <= editor_visibility_zone[1] + editor_visibility_zone[3]
            and rect[1] + rect[3] >= editor_visibility_zone[1]
        )

    def snap_coordinates(self, point: Point) -> Point:
        # Only allow 0 and 0.5 coordinates in each cell
        return Point(
            round(point.x * 2) / 2,
            round(point.y * 2) / 2,
        )

    def draw_line(self, line: Line, color=(255, 255, 255)):
        pos_point1 = self.world_point_to_screen_position(line.point1)
        pos_point2 = self.world_point_to_screen_position(line.point2)
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

        if not self.in_view_screen(self.mouse_x, self.mouse_y):
            return

        if mouse_right_click_press and not self.placing_or_moving:
            # Remove
            nearest_element_position = self.find_nearest_object_position(
                self.screen_position_to_world_point(self.mouse_x, self.mouse_y)
            )
            if nearest_element_position is not None:
                self.delete_element_containing_point(nearest_element_position)
            return

        match self.editor_state:
            case EditorState.PLACE:
                if mouse_left_click_press and not self.placing_or_moving:
                    # Place element
                    self.placing_or_moving = True
                    self.selected_elements.append(self.position_aimed)
                elif mouse_left_click_release and self.placing_or_moving:
                    # Complete place
                    if len(self.selected_elements) > 0:
                        if self.selected_item in wall_items:
                            if self.selected_elements[-1] != self.position_aimed:
                                self.walls.append(
                                    Wall(
                                        self.selected_item,
                                        Line(
                                            self.selected_elements[-1],
                                            self.position_aimed,
                                        ),
                                    )
                                )
                        else:
                            match self.selected_item:
                                case Item.BARREL_SHORT:
                                    self.entities.append(
                                        BarrelShort(self.position_aimed)
                                    )
                                case Item.BARREL_TALL:
                                    self.entities.append(
                                        BarrelTall(self.position_aimed)
                                    )
                                case Item.SPAWN_POINT:
                                    self.spawn_points.append(self.position_aimed)

                        self.selected_elements = []
                    self.placing_or_moving = False
                if mouse_right_click_press and self.placing_or_moving:
                    # Cancel place
                    self.cancel_placing_or_moving()
            case EditorState.MOVE:
                if mouse_left_click_press and not self.placing_or_moving:
                    # Find nearest element
                    nearest_element_position = self.find_nearest_object_position(
                        self.screen_position_to_world_point(self.mouse_x, self.mouse_y)
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
                    if len(self.selected_elements) > 0:
                        self.selected_elements[-1].x = self.position_aimed.x
                        self.selected_elements[-1].y = self.position_aimed.y

    def find_nearest_object_position(self, point: Point) -> Point | None:
        # [(point, distance)]
        objects_distance = []

        for entity in self.entities:
            distance = distance_points(point, entity.position)
            if distance <= self.min_selection_distance:
                objects_distance.append((entity.position, distance))

        for wall in self.walls:
            line = wall.get_line()
            for line_point in [line.point1, line.point2]:
                distance = distance_points(point, line_point)
                if distance <= self.min_selection_distance:
                    objects_distance.append((line_point, distance))

        for spawn_point in self.spawn_points:
            distance = distance_points(point, spawn_point)
            if distance <= self.min_selection_distance:
                objects_distance.append((spawn_point, distance))

        # Sort by distance
        objects_distance.sort(key=lambda element: element[1])

        if len(objects_distance) > 0:
            return objects_distance[0][0]

        return None

    def delete_element_containing_point(self, point: Point):
        for entity in self.entities:
            if entity.position == point:
                self.entities.remove(entity)
                return

        for wall in self.walls:
            line = wall.get_line()
            if line.point1 == point or line.point2 == point:
                self.walls.remove(wall)
                return

        for spawn_point in self.spawn_points:
            if spawn_point == point:
                self.spawn_points.remove(spawn_point)
                return

    def cancel_placing_or_moving(self):
        match self.editor_state:
            case EditorState.PLACE:
                pass
            case EditorState.MOVE:
                if len(self.selected_elements) > 1:
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

        self.position_aimed = self.screen_position_to_world_point(
            self.mouse_x, self.mouse_y
        )
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
                if self.in_view_screen(self.mouse_x, self.mouse_y):
                    self.cell_size = min(
                        self.max_cell_size, self.cell_size + self.scroll_step
                    )
            elif event.id == Event.MOUSE_SCROLL_DOWN:
                if self.in_view_screen(self.mouse_x, self.mouse_y):
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
        point = self.world_point_to_screen_position(self.position_aimed)
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
        for wall in self.walls:
            line = wall.get_line()
            line_rect = (
                min(line.point1.x, line.point2.x),
                min(line.point1.y, line.point2.y),
                abs(line.point2.x - line.point1.x),
                abs(line.point2.y - line.point1.y),
            )

            if self.in_view_world_rect(line_rect):
                self.draw_line(line, (192, 192, 192))
                for point in [line.point1, line.point2]:
                    point_position = self.world_point_to_screen_position(point)
                    pygame.draw.circle(
                        self.surface,
                        (255, 255, 255),
                        (
                            resize(point_position[0], "x"),
                            resize(point_position[1], "y"),
                        ),
                        resize(0.1 * self.cell_size, "x"),
                    )

        for entity in self.entities:
            entity_radius = type(entity).entity_radius()
            entity_rect = (
                entity.position.x - entity_radius,
                entity.position.y - entity_radius,
                entity_radius * 2,
                entity_radius * 2,
            )

            if self.in_view_world_rect(entity_rect):
                entity_position = self.world_point_to_screen_position(entity.position)
                pygame.draw.circle(
                    self.surface,
                    (255, 255, 255),
                    (
                        resize(
                            entity_position[0],
                            "x",
                        ),
                        resize(
                            entity_position[1],
                            "y",
                        ),
                    ),
                    resize(entity_radius * self.cell_size, "x"),
                )

        for spawn_point in self.spawn_points:
            spawn_point_radius = 0.25
            spawn_point_rect = (
                spawn_point.x - spawn_point_radius,
                spawn_point.y - spawn_point_radius,
                spawn_point_radius * 2,
                spawn_point_radius * 2,
            )

            if self.in_view_world_rect(spawn_point_rect):
                spawn_point_position = self.world_point_to_screen_position(spawn_point)
                pygame.draw.circle(
                    self.surface,
                    (128, 255, 128),
                    (
                        resize(
                            spawn_point_position[0],
                            "x",
                        ),
                        resize(
                            spawn_point_position[1],
                            "y",
                        ),
                    ),
                    resize(0.25 * self.cell_size, "x"),
                )

        # Preview element creation
        if self.editor_state == EditorState.PLACE:
            if self.selected_item in wall_items:
                if len(self.selected_elements) > 0:
                    color = (128, 128, 128)

                    self.draw_line(
                        Line(self.selected_elements[-1], self.position_aimed),
                        color,
                    )
                    for point in [self.selected_elements[-1], self.position_aimed]:
                        point_position = self.world_point_to_screen_position(point)
                        pygame.draw.circle(
                            self.surface,
                            color,
                            (
                                resize(point_position[0], "x"),
                                resize(point_position[1], "y"),
                            ),
                            resize(0.1 * self.cell_size, "x"),
                        )
            else:
                if self.placing_or_moving:
                    # Display cross
                    cross_radius = 0.2
                    self.draw_line(
                        Line(
                            Point(
                                self.position_aimed.x - cross_radius,
                                self.position_aimed.y - cross_radius,
                            ),
                            Point(
                                self.position_aimed.x + cross_radius,
                                self.position_aimed.y + cross_radius,
                            ),
                        ),
                        (128, 128, 128),
                    )
                    self.draw_line(
                        Line(
                            Point(
                                self.position_aimed.x + cross_radius,
                                self.position_aimed.y - cross_radius,
                            ),
                            Point(
                                self.position_aimed.x - cross_radius,
                                self.position_aimed.y + cross_radius,
                            ),
                        ),
                        (128, 128, 128),
                    )

        # Proximity indicator
        if not self.placing_or_moving:
            nearest_element_position = self.find_nearest_object_position(
                self.screen_position_to_world_point(self.mouse_x, self.mouse_y)
            )
            if nearest_element_position is not None:
                point_position = self.world_point_to_screen_position(
                    nearest_element_position
                )
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
