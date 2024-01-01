import pygame

from ....configuration import DEFAULT_FONT, VARIABLES
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ...resize import resize
from ...Text import Text
from ..Button import Button, ButtonState
from ..Component import Component
from .EditorState import EditorState


class ToolBar(Component):
    """Level editor tool bar component"""

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

        self.set_original_size(1920, 150)

        self.mouse_x = 0
        self.mouse_y = 0

        # Create buttons
        margin = 20
        button_size = self.original_height - 2 * margin
        self.buttons = [
            # Quit
            Button(
                margin,
                margin,
                button_size,
                button_size,
                action=self.quit,
            ),
            # Load
            Button(
                button_size + 2 * margin,
                margin,
                button_size,
                button_size,
            ),
            # Save
            Button(
                2 * button_size + 3 * margin,
                margin,
                button_size,
                button_size,
            ),
            # Place
            Button(
                960 - button_size / 2 - 2 * self.original_height + 2 * margin,
                margin,
                button_size,
                button_size,
                action=self.set_editor_state_place,
            ),
            # Move
            Button(
                960 - button_size / 2 - self.original_height + margin,
                margin,
                button_size,
                button_size,
                action=self.set_editor_state_move,
            ),
            # Snap to grid
            Button(
                960 + button_size / 2 + margin,
                margin,
                button_size,
                button_size,
                action=lambda: setattr(self, "snap_to_grid", not self.snap_to_grid),
            ),
            # Show grid
            Button(
                960 + button_size / 2 + self.original_height,
                margin,
                button_size,
                button_size,
                action=lambda: setattr(self, "show_grid", not self.show_grid),
            ),
            # Preview
            Button(
                960 + button_size / 2 + 2 * self.original_height - margin,
                margin,
                button_size,
                button_size,
                action=lambda: setattr(self, "preview_player", not self.preview_player),
            ),
            # Help
            Button(
                1920 - (self.original_height - margin),
                margin,
                button_size,
                button_size,
            ),
        ]

        self.snap_to_grid = True
        self.show_grid = True
        self.preview_player = False

        self.editor_state = EditorState.PLACE

        self.update(data)

    def get_editor_state(self) -> EditorState:
        return self.editor_state

    def set_editor_state_place(self):
        self.editor_state = EditorState.PLACE

    def set_editor_state_move(self):
        self.editor_state = EditorState.MOVE

    def get_view_variables(self) -> tuple[bool, bool, bool]:
        return self.snap_to_grid, self.show_grid, self.preview_player

    def quit(self):
        VARIABLES.level_editor = False

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

        mouse_press = False
        mouse_release = False

        for event in events:
            if event.id == Event.MOUSE_LEFT_CLICK_PRESS:
                mouse_press = True
            elif event.id == Event.MOUSE_LEFT_CLICK_RELEASE:
                mouse_release = True

        for button in self.buttons:
            button.update(self.mouse_x, self.mouse_y)
            if mouse_press:
                button.click_press()
            elif mouse_release:
                button.click_release()

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0))

        for button in self.buttons:
            button_pos = button.get_pos()
            button_state = button.get_state()

            color = (64, 64, 64)
            if button_state == ButtonState.HOVERED:
                color = (128, 128, 128)
            elif button_state == ButtonState.PRESSED:
                color = (255, 255, 255)

            pygame.draw.rect(
                self.surface,
                color,
                (
                    resize(button_pos[0], "x"),
                    resize(button_pos[1], "y"),
                    resize(button_pos[2], "x"),
                    resize(button_pos[3], "y"),
                ),
            )

        super().render()
