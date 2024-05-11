import pygame

from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...Button import Button, ButtonState
from ...resize import resize
from ..Component import Component


class PauseMenu(Component):
    """Pause menu component"""

    def __init__(
        self,
        data=[],
    ):
        super().__init__()

        self.set_original_size(1920, 1080)

        self.mouse_x = 0
        self.mouse_y = 0

        self.resume_clicked = False
        self.quit_clicked = False

        button_width = 400
        button_height = 150

        # Create buttons
        self.buttons = [
            Button(
                960 - button_width / 2,
                1080 - button_height * 5,
                button_width,
                button_height,
                content=self.language.get(LanguageKey.MENU_PAUSE_RESUME),
                action=lambda: setattr(self, "resume_clicked", True),
            ),
            Button(
                960 - button_width / 2,
                1080 - button_height * 3,
                button_width,
                button_height,
                content=self.language.get(LanguageKey.MENU_PAUSE_QUIT),
                action=lambda: setattr(self, "quit_clicked", True),
            ),
        ]

        self.update(data)

    def get_status(self):
        return self.resume_clicked, self.quit_clicked

    def update(self, events: list[EventInstance]):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        self.resume_clicked = False
        self.quit_clicked = False

        mouse_press = False
        mouse_release = False

        for event in events:
            if event.id == Event.MOUSE_MOVE:
                self.mouse_x = event.data[0]
                self.mouse_y = event.data[1]
            elif event.id == Event.MOUSE_LEFT_CLICK_PRESS:
                mouse_press = True
            elif event.id == Event.MOUSE_LEFT_CLICK_RELEASE:
                mouse_release = True

        for i in range(len(self.buttons)):
            button = self.buttons[i]

            button.update(self.mouse_x, self.mouse_y)
            if mouse_press:
                button.click_press()
            elif mouse_release:
                button.click_release()

        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 128))

        pause_text = self.text.get_surface(
            self.language.get(LanguageKey.MENU_PAUSE_PAUSE),
            50,
            (255, 255, 255),
        )
        self.surface.blit(
            pause_text,
            (resize(960, "x") - pause_text.get_width() / 2, resize(100, "y")),
        )
        second_pause_text = self.text.get_surface(
            self.language.get(LanguageKey.MENU_PAUSE_INFORMATION),
            40,
            (192, 192, 192),
        )
        self.surface.blit(
            second_pause_text,
            (resize(960, "x") - second_pause_text.get_width() / 2, resize(175, "y")),
        )

        for i in range(len(self.buttons)):
            button = self.buttons[i]

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
                50,
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
