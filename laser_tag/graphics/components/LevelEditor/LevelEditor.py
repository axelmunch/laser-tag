import json

from ....configuration import LEVEL_EDITOR_WORLD_FILE
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....game.load_world import load_world
from ...resize import resize
from ..Component import Component
from .ItemMenu import ItemMenu
from .Toolbar import Toolbar
from .View import View


class LevelEditor(Component):
    """Level editor component"""

    def __init__(self):
        self.toolbar = Toolbar(load_action=self.load, save_action=self.save)
        self.item_menu = ItemMenu()
        self.view = View()
        self.components = [
            self.toolbar,
            self.item_menu,
            self.view,
        ]

        super().__init__()

        self.set_original_size(1920, 1080)

        self.mouse_x = 0
        self.mouse_y = 0

        self.toolbar_position = (0, 0)
        self.item_menu_position = (0, 1080 - self.item_menu.get_size()[1])
        self.view_position = (self.item_menu.get_size()[0], self.toolbar.get_size()[1])

        self.update()

    def resize(self):
        super().resize()

        for component in self.components:
            component.resize()

    def load(self):
        map_data = load_world(LEVEL_EDITOR_WORLD_FILE)

        self.view.set_map_data(map_data)

    def save(self):
        data = self.view.get_map_data()

        minimum_x = self.minimum_y = None

        for wall in data["walls"]:
            line = wall.get_line()
            if minimum_x is None:
                minimum_x = line.point1.x
                minimum_y = line.point1.y
            minimum_x = min(minimum_x, line.point1.x, line.point2.x)
            minimum_y = min(minimum_y, line.point1.y, line.point2.y)

        for entity in data["entities"]:
            if minimum_x is None:
                minimum_x = entity.position.x
                minimum_y = entity.position.y
            minimum_x = min(minimum_x, entity.position.x)
            minimum_y = min(minimum_y, entity.position.y)

        for spawn_point in data["spawn_points"]:
            if minimum_x is None:
                minimum_x = spawn_point.x
                minimum_y = spawn_point.y
            minimum_x = min(minimum_x, spawn_point.x)
            minimum_y = min(minimum_y, spawn_point.y)

        # Shift all values to positive
        if minimum_x is not None:
            for wall in data["walls"]:
                line = wall.get_line()
                line.point1.x -= minimum_x
                line.point1.y -= minimum_y
                line.point2.x -= minimum_x
                line.point2.y -= minimum_y

            for entity in data["entities"]:
                entity.position.x -= minimum_x
                entity.position.y -= minimum_y

            for spawn_point in data["spawn_points"]:
                spawn_point.x -= minimum_x
                spawn_point.y -= minimum_y

        LEVEL_EDITOR_WORLD_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LEVEL_EDITOR_WORLD_FILE, "w") as file:
            json.dump(data, file, indent=4, default=repr)
            file.write("\n")

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        self.data = events
        for event in self.data:
            if event.id == Event.MOUSE_MOVE:
                self.mouse_x = event.data[0]
                self.mouse_y = event.data[1]

        # Toolbar
        self.toolbar.update(
            self.data,
            (self.toolbar_position[0], self.toolbar_position[1]),
        )

        # Item menu
        self.item_menu.update(
            self.data,
            (self.item_menu_position[0], self.item_menu_position[1]),
        )

        # View
        self.view.set_editor_state(self.toolbar.get_editor_state())
        self.view.set_selected_item(self.item_menu.get_selected_item())
        variables = self.toolbar.get_view_variables()
        self.view.set_view_variables(variables[0], variables[1], variables[2])

        self.view.update(self.data, (self.view_position[0], self.view_position[1]))

        super().update()

    def render(self):
        self.surface.fill((255, 255, 255, 64))

        self.surface.blit(
            self.toolbar.get(),
            (
                resize(self.toolbar_position[0], "x"),
                resize(self.toolbar_position[1], "y"),
            ),
        )

        self.surface.blit(
            self.item_menu.get(),
            (
                resize(self.item_menu_position[0], "x"),
                resize(self.item_menu_position[1], "y"),
            ),
        )

        self.surface.blit(
            self.view.get(),
            (resize(self.view_position[0], "x"), resize(self.view_position[1], "y")),
        )

        super().render()
