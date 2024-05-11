import pygame

from ....configuration import VARIABLES
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...Button import Button, ButtonState
from ...resize import resize
from ..Component import Component
from .EditorState import EditorState


class Toolbar(Component):
    """Level editor toolbar component"""

    def __init__(
        self,
        data=[],
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
        self.preview_player = False

        # Create buttons
        margin = 20
        button_size = self.original_height - 2 * margin
        self.place_button = Button(
            960 - button_size / 2 - 2 * self.original_height + 2 * margin,
            margin,
            button_size,
            button_size,
            content=self.language.get(LanguageKey.LEVEL_EDITOR_PLACE),
            action=lambda: setattr(self, "editor_state", EditorState.PLACE),
        )
        self.move_button = Button(
            960 - button_size / 2 - self.original_height + margin,
            margin,
            button_size,
            button_size,
            content=self.language.get(LanguageKey.LEVEL_EDITOR_MOVE),
            action=lambda: setattr(self, "editor_state", EditorState.MOVE),
        )
        self.snap_to_grid_button = Button(
            960 + button_size / 2 + margin,
            margin,
            button_size,
            button_size,
            content=self.language.get(LanguageKey.LEVEL_EDITOR_SNAP),
            action=lambda: setattr(self, "snap_to_grid", not self.snap_to_grid),
        )
        self.show_grid_button = Button(
            960 + button_size / 2 + self.original_height,
            margin,
            button_size,
            button_size,
            content=self.language.get(LanguageKey.LEVEL_EDITOR_GRID),
            action=lambda: setattr(self, "show_grid", not self.show_grid),
        )
        self.preview_player_button = Button(
            960 + button_size / 2 + 2 * self.original_height - margin,
            margin,
            button_size,
            button_size,
            content=self.language.get(LanguageKey.LEVEL_EDITOR_PREVIEW),
            action=lambda: setattr(self, "preview_player", not self.preview_player),
        )
        self.buttons = [
            # Quit
            Button(
                margin,
                margin,
                button_size,
                button_size,
                content=self.language.get(LanguageKey.LEVEL_EDITOR_QUIT),
                action=self.quit,
            ),
            # Load
            Button(
                button_size + 2 * margin,
                margin,
                button_size,
                button_size,
                content=self.language.get(LanguageKey.LEVEL_EDITOR_LOAD),
                action=load_action,
            ),
            # Save
            Button(
                2 * button_size + 3 * margin,
                margin,
                button_size,
                button_size,
                content=self.language.get(LanguageKey.LEVEL_EDITOR_SAVE),
                action=save_action,
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
            self.preview_player_button,
            # Help
            Button(
                1920 - (self.original_height - margin),
                margin,
                button_size,
                button_size,
                content=self.language.get(LanguageKey.LEVEL_EDITOR_HELP),
                disabled=True,
            ),
        ]

        self.update(data)

    def get_editor_state(self) -> EditorState:
        return self.editor_state

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

        # Border on selected elements
        selected_buttons = []
        if self.editor_state == EditorState.PLACE:
            selected_buttons.append(self.place_button)
        else:
            selected_buttons.append(self.move_button)
        if self.snap_to_grid:
            selected_buttons.append(self.snap_to_grid_button)
        if self.show_grid:
            selected_buttons.append(self.show_grid_button)
        if self.preview_player:
            selected_buttons.append(self.preview_player_button)

        for button in selected_buttons:
            button_pos = button.get_pos()

            border_size = 6
            pygame.draw.rect(
                self.surface,
                (192, 192, 192),
                (
                    resize(button_pos[0] - border_size, "x"),
                    resize(button_pos[1] - border_size, "y"),
                    resize(button_pos[2] + border_size * 2, "x"),
                    resize(button_pos[3] + border_size * 2, "y"),
                ),
            )

        for button in self.buttons:
            button_pos = button.get_pos()
            button_state = button.get_state()
            button_content = button.get_content()

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

            text_surface = self.text.get_surface(
                button_content,
                30,
                (255, 255, 255),
            )
            self.surface.blit(
                text_surface,
                (
                    resize(
                        button_pos[0] + button_pos[2] / 2,
                        "x",
                    )
                    - text_surface.get_width() / 2,
                    resize(
                        button_pos[1] + button_pos[3] / 2,
                        "y",
                    )
                    - text_surface.get_height() / 2,
                ),
            )

        super().render()
