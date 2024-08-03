import pygame

from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....game.Game import Game
from ....game.Mode import Mode
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import ButtonType, GraphicalButton
from .Menu import Menu


class ModeTeamSelectionMenu(Component, Menu):
    """Mode and team selection menu component"""

    def __init__(self, game: Game):
        Component.__init__(self)
        Menu.__init__(self)

        self.game = game

        self.set_original_size(1920, 1080)

        self.menu_box_width = 1920 - 500
        self.menu_box_height = 1080 - 200
        self.border_margin = 50
        self.button_width = (self.menu_box_width - 20 * 5 - self.border_margin * 2) / 5
        self.button_height = 100

        self.back_button = GraphicalButton(
            960 + self.menu_box_width / 2 - 50 - self.button_width,
            540 + self.menu_box_height / 2 - self.button_height - 50,
            self.button_width,
            self.button_height,
            text="START",
            action=lambda: self.add_event(EventInstance(Event.START_GAME)),
        )
        self.teams_button = GraphicalButton(
            960 + self.menu_box_width / 4 - self.button_width / 2,
            540 - self.menu_box_height / 2 + self.border_margin,
            self.button_width,
            self.button_height,
            text="Teams",
            action=lambda: self.switch_page(1),
            type=ButtonType.SETTINGS_CATEGORY,
        )

        self.default_elements = [self.back_button]

        self.pages_buttons = [
            GraphicalButton(
                960 - self.menu_box_width / 4 - self.button_width / 2,
                540 - self.menu_box_height / 2 + self.border_margin,
                self.button_width,
                self.button_height,
                text="Game mode",
                action=lambda: self.switch_page(0),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
            self.teams_button,
        ]
        self.pages_elements = [[], []]
        self.elements = []

        self.selected_mode = Mode.SOLO

        self.current_page = 0
        self.refresh()

        self.update()

    def resize(self):
        try:
            for page_elements in self.pages_elements:
                for element in page_elements:
                    element.resize()
        except AttributeError:
            pass

        Menu.resize(self)
        Component.resize(self)

    def select_mode(self, mode: Mode):
        if self.selected_mode != mode:
            self.selected_mode = mode
            self.add_event(EventInstance(Event.CHANGE_GAME_MODE, mode))
            self.refresh()

    def refresh(self):
        self.pages_elements = [
            [
                GraphicalButton(
                    960 - self.menu_box_width / 6 - self.button_width / 2,
                    540 - self.menu_box_height / 2 + self.border_margin + 215,
                    self.button_width,
                    self.button_height,
                    text="SOLO",
                    action=lambda: self.select_mode(Mode.SOLO),
                    type=ButtonType.GAME_MODE,
                    selected=self.selected_mode == Mode.SOLO,
                ),
                GraphicalButton(
                    960 + self.menu_box_width / 6 - self.button_width / 2,
                    540 - self.menu_box_height / 2 + self.border_margin + 215,
                    self.button_width,
                    self.button_height,
                    text="TEAM",
                    action=lambda: self.select_mode(Mode.TEAM),
                    type=ButtonType.GAME_MODE,
                    selected=self.selected_mode == Mode.TEAM,
                ),
                GraphicalButton(
                    960 - self.menu_box_width / 6 - self.button_width / 2,
                    540 - self.menu_box_height / 2 + self.border_margin + 465,
                    self.button_width,
                    self.button_height,
                    text="SOLO_ELIMINATION",
                    action=lambda: self.select_mode(Mode.SOLO_ELIMINATION),
                    type=ButtonType.GAME_MODE,
                    selected=self.selected_mode == Mode.SOLO_ELIMINATION,
                ),
                GraphicalButton(
                    960 + self.menu_box_width / 6 - self.button_width / 2,
                    540 - self.menu_box_height / 2 + self.border_margin + 465,
                    self.button_width,
                    self.button_height,
                    text="TEAM_ELIMINATION",
                    action=lambda: self.select_mode(Mode.TEAM_ELIMINATION),
                    type=ButtonType.GAME_MODE,
                    selected=self.selected_mode == Mode.TEAM_ELIMINATION,
                ),
            ],
            [],
        ]

        no_teams_mode = (
            self.selected_mode == Mode.SOLO
            or self.selected_mode == Mode.SOLO_ELIMINATION
        )
        self.teams_button.set_disabled(no_teams_mode)
        if no_teams_mode:
            self.current_page = 0

        self.switch_page(self.current_page)

    def switch_page(self, page: int):
        self.current_page = page
        # Default
        self.elements = self.default_elements[:]

        for i, element in enumerate(self.pages_buttons):
            element.set_selected(i == page)
            self.elements.append(element)

        for element in self.pages_elements[page]:
            self.elements.append(element)

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        for event in events:
            if event.id == Event.CHANGE_GAME_MODE:
                self.selected_mode = Mode(event.data)
                self.refresh()

        Menu.update(self, events, no_escape=True)
        Component.update(self)

        if self.game.game_mode.is_game_started():
            self.game.game_paused = False
            self.set_active(False)

    def render(self):
        self.surface.fill((0, 0, 0, 128))

        pygame.draw.rect(
            self.surface,
            (0, 100, 0),
            (
                resize(960 - self.menu_box_width / 2, "x"),
                resize(540 - self.menu_box_height / 2, "y"),
                resize(self.menu_box_width, "x"),
                resize(self.menu_box_height, "y"),
            ),
        )

        selection_title_text = self.text.get_surface(
            self.language.get(LanguageKey.MENU_SETTINGS_TITLE), 50, (255, 255, 255)
        )
        self.surface.blit(
            selection_title_text,
            (
                resize(960, "x") - selection_title_text.get_width() / 2,
                resize(540 - self.menu_box_height / 2 + 20, "y"),
            ),
        )

        for element in self.elements:
            self.surface.blit(
                element.get(), (resize(element.x, "x"), resize(element.y, "y"))
            )

        super().render()
