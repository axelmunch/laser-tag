from ....configuration import VARIABLES
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import ButtonType, GraphicalButton
from .EditorState import EditorState


class Toolbar(Component):
    """Level editor toolbar component"""

    def __init__(
        self,
        load_action=None,
        save_action=None,
    ):
        super().__init__()

        self.set_original_size(1920, 150)

        self.mouse_x = 0
        self.mouse_y = 0

        self.editor_state = EditorState.PLACE

        self.snap_to_grid = True
        self.show_grid = True
        self.preview = False

        # Create buttons
        margin = 20
        button_size = self.original_height - 2 * margin
        self.place_button = GraphicalButton(
            960 - button_size / 2 - 2 * self.original_height + 2 * margin,
            margin,
            button_size,
            button_size,
            text_key=LanguageKey.LEVEL_EDITOR_PLACE,
            action=lambda: setattr(self, "editor_state", EditorState.PLACE),
            type=ButtonType.LEVEL_EDITOR,
        )
        self.move_button = GraphicalButton(
            960 - button_size / 2 - self.original_height + margin,
            margin,
            button_size,
            button_size,
            text_key=LanguageKey.LEVEL_EDITOR_MOVE,
            action=lambda: setattr(self, "editor_state", EditorState.MOVE),
            type=ButtonType.LEVEL_EDITOR,
        )
        self.snap_to_grid_button = GraphicalButton(
            960 + button_size / 2 + margin,
            margin,
            button_size,
            button_size,
            text_key=LanguageKey.LEVEL_EDITOR_SNAP,
            action=lambda: setattr(self, "snap_to_grid", not self.snap_to_grid),
            type=ButtonType.LEVEL_EDITOR,
        )
        self.show_grid_button = GraphicalButton(
            960 + button_size / 2 + self.original_height,
            margin,
            button_size,
            button_size,
            text_key=LanguageKey.LEVEL_EDITOR_GRID,
            action=lambda: setattr(self, "show_grid", not self.show_grid),
            type=ButtonType.LEVEL_EDITOR,
        )
        self.preview_button = GraphicalButton(
            960 + button_size / 2 + 2 * self.original_height - margin,
            margin,
            button_size,
            button_size,
            text_key=LanguageKey.LEVEL_EDITOR_PREVIEW,
            action=lambda: setattr(self, "preview", not self.preview),
            type=ButtonType.LEVEL_EDITOR,
        )
        self.buttons = [
            # Quit
            GraphicalButton(
                margin,
                margin,
                button_size,
                button_size,
                text_key=LanguageKey.LEVEL_EDITOR_QUIT,
                action=self.quit,
                type=ButtonType.LEVEL_EDITOR,
            ),
            # Load
            GraphicalButton(
                button_size + 2 * margin,
                margin,
                button_size,
                button_size,
                text_key=LanguageKey.LEVEL_EDITOR_LOAD,
                action=load_action,
                type=ButtonType.LEVEL_EDITOR,
            ),
            # Save
            GraphicalButton(
                2 * button_size + 3 * margin,
                margin,
                button_size,
                button_size,
                text_key=LanguageKey.LEVEL_EDITOR_SAVE,
                action=save_action,
                type=ButtonType.LEVEL_EDITOR,
            ),
            # Place
            self.place_button,
            # Move
            self.move_button,
            # Snap to grid
            self.snap_to_grid_button,
            # Show grid
            self.show_grid_button,
            # Preview player
            self.preview_button,
            # Help
            GraphicalButton(
                1920 - (self.original_height - margin),
                margin,
                button_size,
                button_size,
                text_key=LanguageKey.LEVEL_EDITOR_HELP,
                disabled=True,
                type=ButtonType.LEVEL_EDITOR,
            ),
        ]

        self.update()

    def get_editor_state(self) -> EditorState:
        return self.editor_state

    def get_view_variables(self) -> tuple[bool, bool, bool]:
        return self.snap_to_grid, self.show_grid, self.preview

    def quit(self):
        VARIABLES.level_editor = False

    def update(
        self,
        events: list[EventInstance] = [],
        relative_offset: tuple[int, int] = (0, 0),
    ):
        """
        Update the component

        Parameters:
            events (list): Events
            relative_offset (tuple): Component position on the screen
        """

        for event in events:
            if event.id == Event.MOUSE_MOVE:
                self.mouse_x = event.data[0]
                self.mouse_y = event.data[1]

        for button in self.buttons:
            button.set_relative_offset(relative_offset[0], relative_offset[1])
            button.update(events)
            button.set_selected(False)

        if self.editor_state == EditorState.PLACE:
            self.place_button.set_selected(True)
        else:
            self.move_button.set_selected(True)
        if self.snap_to_grid:
            self.snap_to_grid_button.set_selected(True)
        if self.show_grid:
            self.show_grid_button.set_selected(True)
        if self.preview:
            self.preview_button.set_selected(True)

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0))

        for button in self.buttons:
            self.surface.blit(
                button.get(),
                (resize(button.x, "x"), resize(button.y, "y")),
            )

        super().render()
