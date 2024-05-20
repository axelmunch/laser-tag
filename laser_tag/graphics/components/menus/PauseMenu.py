from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import GraphicalButton
from .Confirmation import Confirmation
from .Menu import Menu
from .Menus import Menus
from .SettingsMenu import SettingsMenu


class PauseMenu(Component, Menu):
    """Pause menu component"""

    def __init__(self, callback_resume=None, callback_quit=None):
        Component.__init__(self)
        Menu.__init__(self)

        self.set_original_size(1920, 1080)

        self.callback_resume = callback_resume
        self.callback_quit = callback_quit

        button_width = 400
        button_height = 150

        # Create buttons
        self.elements = [
            GraphicalButton(
                960 - button_width / 2,
                1080 - button_height * 4.5,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_PAUSE_RESUME,
                action=self.resume,
            ),
            GraphicalButton(
                960 - button_width / 2,
                1080 - button_height * 3,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_PAUSE_SETTINGS,
                action=self.settings,
            ),
            GraphicalButton(
                960 - button_width / 2,
                1080 - button_height * 1.5,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_PAUSE_QUIT,
                action=lambda: Menus().open_menu(
                    Confirmation(
                        LanguageKey.MENU_CONFIRMATION_QUIT_GAME, callback_yes=self.quit
                    )
                ),
            ),
        ]

        self.update()

    def resize(self):
        super().resize()

        try:
            for element in self.elements:
                element.resize()
        except AttributeError:
            pass

    def resume(self):
        if self.callback_resume is not None:
            self.callback_resume()
        self.set_active(False)

    def settings(self):
        Menus().open_menu(SettingsMenu())

    def quit(self):
        if self.callback_quit is not None:
            self.callback_quit()
        self.set_active(False)

    def deactivate_event(self):
        self.resume()

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        Menu.update(self, events)
        Component.update(self)

    def render(self):
        self.surface.fill((0, 0, 0, 128))

        pause_text = self.text.get_surface(
            self.language.get(LanguageKey.MENU_PAUSE_TITLE),
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

        for element in self.elements:
            self.surface.blit(
                element.get(),
                (resize(element.x, "x"), resize(element.y, "y")),
            )

        super().render()
