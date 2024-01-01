from ....configuration import DEFAULT_FONT
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ...resize import resize
from ...Text import Text
from ..Component import Component
from .ItemMenu import ItemMenu
from .ToolBar import ToolBar
from .View import View


class LevelEditor(Component):
    """Level editor component"""

    def __init__(
        self,
        data=[],
    ):
        self.tool_bar = ToolBar()
        self.item_menu = ItemMenu()
        self.view = View()
        self.components = [
            self.tool_bar,
            self.item_menu,
            self.view,
        ]

        super().__init__()

        self.text = Text(
            DEFAULT_FONT["font"],
            DEFAULT_FONT["font_is_file"],
            DEFAULT_FONT["size_multiplier"],
        )

        self.set_original_size(1920, 1080)

        self.mouse_x = 0
        self.mouse_y = 0

        self.tool_bar_position = (0, 0)
        self.item_menu_position = (0, 1080 - self.item_menu.get_size()[1])
        self.view_position = (self.item_menu.get_size()[0], self.tool_bar.get_size()[1])

        self.update(data)

    def resize(self):
        super().resize()

        for component in self.components:
            component.resize()

    def update(self, events: list[EventInstance]):
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

        # Tool bar
        self.tool_bar.update(
            self.data,
            (
                self.mouse_x - self.tool_bar_position[0],
                self.mouse_y - self.tool_bar_position[1],
            ),
        )

        # Item menu
        self.item_menu.update(
            self.data,
            (
                self.mouse_x - self.item_menu_position[0],
                self.mouse_y - self.item_menu_position[1],
            ),
        )

        # View
        self.view.set_editor_state(self.tool_bar.get_editor_state())
        self.view.set_selected_item(self.item_menu.get_selected_item())
        variables = self.tool_bar.get_view_variables()
        self.view.set_view_variables(variables[0], variables[1], variables[2])

        self.view.update(
            self.data,
            (
                self.mouse_x - self.view_position[0],
                self.mouse_y - self.view_position[1],
            ),
        )

        super().update()

    def render(self):
        self.surface.fill((255, 255, 255, 64))

        self.surface.blit(
            self.tool_bar.get(),
            (
                resize(self.tool_bar_position[0], "x"),
                resize(self.tool_bar_position[1], "y"),
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
