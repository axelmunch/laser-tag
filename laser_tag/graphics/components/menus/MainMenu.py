from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import GraphicalButton
from .Confirmation import Confirmation
from .Menu import Menu
from .Menus import Menus


class MainMenu(Component, Menu):
    """Main menu component"""

    def __init__(self, callback_play=None, callback_settings=None, callback_quit=None):
        Component.__init__(self)
        Menu.__init__(self)

        self.set_original_size(1920, 1080)

        self.callback_play = callback_play
        self.callback_settings = callback_settings
        self.callback_quit = callback_quit

        self.can_deactivate = False

        button_width = 400
        button_height = 100

        # Create buttons
        self.elements = [
            GraphicalButton(
                960 - button_width / 2,
                1080 - button_height * 6,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_MAIN_PLAY,
                action=self.play,
            ),
            GraphicalButton(
                960 - button_width / 2,
                1080 - button_height * 4,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_MAIN_SETTINGS,
                action=self.settings,
            ),
            GraphicalButton(
                960 - button_width / 2,
                1080 - button_height * 2,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_MAIN_QUIT,
                action=lambda: Menus().open_menu(
                    Confirmation(
                        LanguageKey.MENU_CONFIRMATION_CLOSE_GAME, callback_yes=self.quit
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

    def play(self):
        if self.callback_play is not None:
            self.callback_play()
        self.can_deactivate = True
        self.set_active(False)

    def settings(self):
        if self.callback_settings is not None:
            self.callback_settings()

    def quit(self):
        if self.callback_quit is not None:
            self.callback_quit()
        self.can_deactivate = True
        self.set_active(False)

    def deactivate_event(self):
        if not self.can_deactivate:
            self.set_active(True)
            Menus().open_menu(
                Confirmation(
                    LanguageKey.MENU_CONFIRMATION_CLOSE_GAME, callback_yes=self.quit
                )
            )

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        Menu.update(self, events)
        Component.update(self)

    def render(self):
        self.surface.fill((0, 0, 0))

        pause_text = self.text.get_surface(
            self.language.get(LanguageKey.GAME_NAME),
            50,
            (255, 255, 255),
        )
        self.surface.blit(
            pause_text,
            (resize(960, "x") - pause_text.get_width() / 2, resize(100, "y")),
        )

        for element in self.elements:
            self.surface.blit(
                element.get(),
                (resize(element.x, "x"), resize(element.y, "y")),
            )

        super().render()
