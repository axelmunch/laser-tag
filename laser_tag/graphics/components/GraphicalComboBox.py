from math import ceil

import pygame

from ...events.Event import Event
from ...events.EventInstance import EventInstance
from ..Button import Button, ButtonState
from ..resize import resize
from .GraphicalElement import GraphicalElement


class GraphicalComboBox(GraphicalElement):
    """Combo box component"""

    def __init__(
        self,
        x: float,
        y: float,
        choices={},
        default_choice=None,
        change_action=None,
        disabled=False,
        selected=False,
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.scroll = 0
        self.choice_width = 250
        self.choice_height = 100
        self.choices = choices
        self.choice = default_choice
        self.change_action = change_action
        self.disabled = disabled
        self.set_selected(selected)
        self.opened = False

        self.relative_offset_x = 0
        self.relative_offset_y = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.max_elements = 2.5

        self.button = Button(
            0,
            0,
            self.choice_width,
            self.choice_height,
            action=self.toggle,
            disabled=self.disabled,
        )

        self.choices_buttons = []
        i = 0
        for key, choice in self.choices.items():
            self.choices_buttons.append(
                Button(
                    0,
                    self.choice_height + i * self.choice_height,
                    self.choice_width,
                    self.choice_height,
                    text=choice,
                    action=lambda i=key: self.select(i),
                    disabled=self.disabled,
                )
            )
            i += 1

        self.set_original_size(self.choice_width, self.choice_height)

        self.set_relative_offset(self.x, self.y)

        self.update()

    def resize(self):
        super().resize()

        try:
            self.button.resize()
            for choice_button in self.choices_buttons:
                choice_button.resize()
        except AttributeError:
            pass

    def set_disabled(self, disabled: bool):
        self.disabled = disabled
        if disabled:
            self.button.disable()
            for choice_button in self.choices_buttons:
                choice_button.disable()
        else:
            self.button.enable()
            for choice_button in self.choices_buttons:
                choice_button.enable()

    def set_relative_offset(self, offset_x: float, offset_y: float):
        self.relative_offset_x = offset_x
        self.relative_offset_y = offset_y

    def toggle(self):
        if self.opened:
            self.close()
        else:
            self.open()

    def open(self):
        self.opened = True
        self.set_original_size(
            self.choice_width,
            min(
                self.choice_height * (self.max_elements + 1),
                self.choice_height + len(self.choices) * self.choice_height,
            ),
        )

    def close(self):
        self.scroll = 0
        self.opened = False
        self.set_original_size(self.choice_width, self.choice_height)

    def select(self, key):
        if not self.opened:
            return

        if self.choice != key:
            self.choice = key
            if self.change_action is not None:
                self.change_action(key)

        self.close()

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        mouse_press = False
        mouse_release = False

        for event in events:
            if event.id == Event.MOUSE_MOVE:
                self.mouse_x = event.data[0] - self.relative_offset_x
                self.mouse_y = event.data[1] - self.relative_offset_y
            elif event.id == Event.MOUSE_LEFT_CLICK_PRESS:
                mouse_press = True
            elif event.id == Event.MOUSE_LEFT_CLICK_RELEASE:
                mouse_release = True
            elif event.id == Event.MOUSE_SCROLL_UP:
                if (
                    self.opened
                    and self.mouse_x >= 0
                    and self.mouse_x <= self.original_width
                    and self.mouse_y >= self.choice_height
                    and self.mouse_y <= self.original_height
                ):
                    self.scroll = max(0, self.scroll - 10)
            elif event.id == Event.MOUSE_SCROLL_DOWN:
                if (
                    self.opened
                    and self.mouse_x >= 0
                    and self.mouse_x <= self.original_width
                    and self.mouse_y >= self.choice_height
                    and self.mouse_y <= self.original_height
                ):
                    self.scroll = max(
                        0,
                        min(
                            len(self.choices_buttons) * self.choice_height
                            - self.choice_height * self.max_elements,
                            self.scroll + 10,
                        ),
                    )

        self.button.update(self.mouse_x, self.mouse_y)

        if mouse_press:
            self.button.click_press()
        elif mouse_release:
            self.button.click_release()

        if self.opened:
            for choice_button in self.choices_buttons:
                choice_button.y = (
                    self.choice_height
                    + (self.choices_buttons.index(choice_button)) * self.choice_height
                    - self.scroll
                )

            if (
                self.mouse_x >= 0
                and self.mouse_x <= self.original_width
                and self.mouse_y >= 0
                and self.mouse_y <= self.original_height
            ):
                for choice_button in self.choices_buttons:
                    if self.mouse_y >= self.choice_height:
                        choice_button.update(self.mouse_x, self.mouse_y)
                        if mouse_press:
                            choice_button.click_press()
                        elif mouse_release:
                            choice_button.click_release()
                    else:
                        choice_button.update(-1, -1)
            else:
                for choice_button in self.choices_buttons:
                    choice_button.update(-1, -1)
                if mouse_press:
                    self.close()

        super().update()

    def render(self):
        text_color = (255, 255, 255)
        text_size = 50

        if self.opened:
            for choice_button in self.choices_buttons:
                button_state = choice_button.get_state()
                button_text = choice_button.get_text()

                color = (64, 64, 64)
                if button_state == ButtonState.HOVERED:
                    color = (128, 128, 128)
                elif button_state == ButtonState.PRESSED:
                    color = (192, 192, 192)

                pygame.draw.rect(
                    self.surface,
                    color,
                    (
                        0,
                        resize(choice_button.y, "y"),
                        resize(self.choice_width, "x"),
                        resize(self.choice_height, "y"),
                    ),
                )

                text_surface = self.text.get_surface(button_text, text_size, text_color)
                self.surface.blit(
                    text_surface,
                    (
                        resize(self.choice_width / 2, "x")
                        - text_surface.get_width() / 2,
                        resize(choice_button.y, "y")
                        + resize(self.choice_height / 2, "y")
                        - text_surface.get_height() / 2,
                    ),
                )

        button_state = self.button.get_state()

        color = (64, 64, 64)
        if button_state == ButtonState.HOVERED:
            color = (128, 128, 128)
        elif button_state == ButtonState.PRESSED:
            color = (192, 192, 192)

        pygame.draw.rect(
            self.surface,
            color,
            (
                0,
                0,
                ceil(resize(self.choice_width, "x")),
                ceil(resize(self.choice_height, "y")),
            ),
        )
        pygame.draw.rect(
            self.surface,
            (0, 0, 0),
            (
                0,
                0,
                ceil(resize(self.choice_width, "x")),
                ceil(resize(self.choice_height, "y")),
            ),
            max(1, int(resize(6, "x"))),
        )

        text_surface = self.text.get_surface(
            self.choices[self.choice] if self.choice is not None else "",
            text_size,
            text_color,
        )
        self.surface.blit(
            text_surface,
            (
                resize(self.choice_width / 2, "x") - text_surface.get_width() / 2,
                resize(self.choice_height / 2, "y") - text_surface.get_height() / 2,
            ),
        )

        if self.is_selected():
            border_size = 6
            pygame.draw.rect(
                self.surface,
                (192, 192, 192),
                (
                    0,
                    0,
                    ceil(resize(self.choice_width, "x")),
                    ceil(resize(self.choice_height, "y")),
                ),
                max(1, int(resize(border_size, "x"))),
            )

        super().render()
