import pygame

from ....entities.Player import Player
from ....events.Event import Event
from ....events.EventInstance import EventInstance
from ....game.Game import Game
from ....game.GameMode import GameMode
from ....game.Mode import Mode, get_mode_language_key
from ....game.Team import Team, get_team_color, get_team_language_key
from ....language.LanguageKey import LanguageKey
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import ButtonType, GraphicalButton
from .Menu import Menu


class ModeTeamSelectionMenu(Component, Menu):
    """Mode and team selection menu component"""

    def __init__(self, game: Game, callback_quit=None):
        Component.__init__(self)
        Menu.__init__(self)

        self.game = game
        self.callback_quit = callback_quit

        self.set_original_size(1920, 1080)

        self.menu_box_width = 1920 - 500
        self.menu_box_height = 1080 - 200
        self.border_margin = 50
        self.button_width = (self.menu_box_width - 20 * 5 - self.border_margin * 2) / 4
        self.button_height = 100

        self.teams_button = GraphicalButton(
            960 + self.menu_box_width / 4 - self.button_width / 2,
            540 - self.menu_box_height / 2 + self.border_margin,
            self.button_width,
            self.button_height,
            text_key=LanguageKey.MENU_SELECTION_TEAMS,
            action=lambda: self.switch_page(1),
            type=ButtonType.SETTINGS_CATEGORY,
        )

        self.default_elements = [
            GraphicalButton(
                960 - self.menu_box_width / 2 + self.border_margin,
                540
                + self.menu_box_height / 2
                - self.button_height
                - self.border_margin,
                self.button_width,
                self.button_height,
                text_key=LanguageKey.MENU_SELECTION_LEAVE,
                action=self.quit,
            ),
            GraphicalButton(
                960 + self.menu_box_width / 2 - self.border_margin - self.button_width,
                540
                + self.menu_box_height / 2
                - self.button_height
                - self.border_margin,
                self.button_width,
                self.button_height,
                text_key=LanguageKey.MENU_SELECTION_START,
                action=lambda: self.add_event(EventInstance(Event.START_GAME)),
            ),
        ]

        self.pages_buttons = [
            GraphicalButton(
                960 - self.menu_box_width / 4 - self.button_width / 2,
                540 - self.menu_box_height / 2 + self.border_margin,
                self.button_width,
                self.button_height,
                text_key=LanguageKey.MENU_SELECTION_GAME_MODE,
                action=lambda: self.switch_page(0),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
            self.teams_button,
        ]
        self.pages_elements = [[], []]
        self.elements = []

        self.selected_mode = self.game.game_mode.game_mode
        self.available_teams = GameMode.get_teams_available(self.selected_mode)
        self.team_areas = {}
        self.players: dict[int, Player] = {}
        self.player_areas = {}
        self.grab_player_id = None

        self.mouse_x = -1
        self.mouse_y = -1

        self.player_count = 0

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
        self.player_count = 0
        mode_button_width = self.button_width * 1.5
        mode_button_height = self.button_height
        self.pages_elements = [
            [
                GraphicalButton(
                    960 - self.menu_box_width / 5 - mode_button_width / 2,
                    540 - self.menu_box_height / 2 + self.border_margin + 215,
                    mode_button_width,
                    mode_button_height,
                    text_key=get_mode_language_key(Mode.SOLO),
                    action=lambda: self.select_mode(Mode.SOLO),
                    type=ButtonType.GAME_MODE,
                    selected=self.selected_mode == Mode.SOLO,
                ),
                GraphicalButton(
                    960 + self.menu_box_width / 5 - mode_button_width / 2,
                    540 - self.menu_box_height / 2 + self.border_margin + 215,
                    mode_button_width,
                    mode_button_height,
                    text_key=get_mode_language_key(Mode.TEAM),
                    action=lambda: self.select_mode(Mode.TEAM),
                    type=ButtonType.GAME_MODE,
                    selected=self.selected_mode == Mode.TEAM,
                ),
                GraphicalButton(
                    960 - self.menu_box_width / 5 - mode_button_width / 2,
                    540 - self.menu_box_height / 2 + self.border_margin + 465,
                    mode_button_width,
                    mode_button_height,
                    text_key=get_mode_language_key(Mode.SOLO_ELIMINATION),
                    action=lambda: self.select_mode(Mode.SOLO_ELIMINATION),
                    type=ButtonType.GAME_MODE,
                    selected=self.selected_mode == Mode.SOLO_ELIMINATION,
                ),
                GraphicalButton(
                    960 + self.menu_box_width / 5 - mode_button_width / 2,
                    540 - self.menu_box_height / 2 + self.border_margin + 465,
                    mode_button_width,
                    mode_button_height,
                    text_key=get_mode_language_key(Mode.TEAM_ELIMINATION),
                    action=lambda: self.select_mode(Mode.TEAM_ELIMINATION),
                    type=ButtonType.GAME_MODE,
                    selected=self.selected_mode == Mode.TEAM_ELIMINATION,
                ),
            ],
            [],
        ]

        no_teams_mode = len(GameMode.get_teams_available(self.selected_mode)) <= 1
        self.teams_button.set_disabled(no_teams_mode)
        if no_teams_mode:
            self.current_page = 0

        # Teams
        self.available_teams = GameMode.get_teams_available(self.selected_mode)
        self.team_areas = {}

        max_line = len(self.available_teams) // 3
        area_width = self.menu_box_width / 4.5
        area_height = 60
        areas_margin = 10
        for index, team in enumerate(self.available_teams):
            line = index // 3 + 3 - max_line - 1
            column = index % 3

            x = (
                960
                - self.menu_box_width / 2
                + self.menu_box_width / 4 * (column + 1)
                - area_width / 2
            )
            y = (
                540
                + self.menu_box_height / 2
                - self.border_margin
                - self.button_height
                - area_height * 3
                - areas_margin * 3
                + line * (area_height + areas_margin)
            )

            self.team_areas[team] = (x, y, area_width, area_height)

        # Players
        self.player_areas = {}
        self.players = {}
        self.grab_player_id = None
        for id, entity in self.game.world.entities.items():
            if isinstance(entity, Player):
                self.players[id] = entity
                self.player_count += 1

        player_width = self.menu_box_width / 4.5
        player_height = 60
        players_margin = 10
        for index, id in enumerate(self.players.keys()):
            line = index // 3
            column = index % 3

            x = (
                960
                - self.menu_box_width / 2
                + self.menu_box_width / 4 * (column + 1)
                - player_width / 2
            )
            y = (
                540
                - self.menu_box_height / 2
                + self.border_margin
                + self.button_height * 2
                + line * (player_height + players_margin)
            )
            self.player_areas[id] = (x, y, player_width, player_height)

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

    def is_hovered(self, rect) -> bool:
        return (
            self.mouse_x - rect[0] >= 0
            and self.mouse_x - rect[0] <= rect[2]
            and self.mouse_y - rect[1] >= 0
            and self.mouse_y - rect[1] <= rect[3]
        )

    def quit(self):
        if self.callback_quit is not None:
            self.callback_quit()
        self.set_active(False)

    def update(self, events: list[EventInstance] = []):
        """
        Update the component

        Parameters:
            events (list): Events
        """

        mouse_press = False
        mouse_release = False

        if self.game.game_mode.game_mode != self.selected_mode:
            self.selected_mode = self.game.game_mode.game_mode
            self.refresh()

        for event in events:
            if (
                event.id == Event.PLAYER_JOIN
                or event.id == Event.PLAYER_LEAVE
                or event.id == Event.CHANGE_PLAYER_TEAM
            ):
                self.refresh()
            elif event.id == Event.MOUSE_MOVE:
                self.mouse_x = event.data[0]
                self.mouse_y = event.data[1]
            elif event.id == Event.MOUSE_LEFT_CLICK_PRESS:
                mouse_press = True
            elif event.id == Event.MOUSE_LEFT_CLICK_RELEASE:
                mouse_release = True

        if self.current_page == 1:
            if mouse_press:
                # Grab player
                if self.grab_player_id is None:
                    for id, area in self.player_areas.items():
                        if self.is_hovered(area):
                            self.grab_player_id = id
                            break
            if mouse_release:
                # Release player
                if self.grab_player_id is not None:
                    for team, area in self.team_areas.items():
                        if self.is_hovered(area):
                            self.add_event(
                                EventInstance(
                                    Event.CHANGE_PLAYER_TEAM,
                                    [self.grab_player_id, team.value],
                                )
                            )
                            break
                    self.grab_player_id = None

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
            self.language.get(LanguageKey.MENU_SELECTION_TITLE), 50, (255, 255, 255)
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

        if self.current_page == 1:
            if len(self.team_areas) > 0 and len(self.player_areas) > 0:
                text_surface = self.text.get_surface(
                    self.language.get(LanguageKey.MENU_SELECTION_PLAYERS),
                    50,
                    (255, 255, 255),
                )
                self.surface.blit(
                    text_surface,
                    (
                        resize(list(self.team_areas.values())[0][0], "x"),
                        resize(list(self.player_areas.values())[0][1] - 10, "y")
                        - text_surface.get_height(),
                    ),
                )

                text_surface = self.text.get_surface(
                    self.language.get(LanguageKey.MENU_SELECTION_TEAMS),
                    50,
                    (255, 255, 255),
                )
                self.surface.blit(
                    text_surface,
                    (
                        resize(list(self.team_areas.values())[0][0], "x"),
                        resize(list(self.team_areas.values())[0][1] - 10, "y")
                        - text_surface.get_height(),
                    ),
                )

            # Teams
            for team, area in self.team_areas.items():
                if not (self.grab_player_id is not None and self.is_hovered(area)):
                    # Team name
                    text_surface = self.text.get_surface(
                        self.language.get(get_team_language_key(team)),
                        30,
                        (255, 255, 255),
                    )
                    self.surface.blit(
                        text_surface,
                        (
                            resize(area[0] + area[2] / 2, "x")
                            - text_surface.get_width() / 2,
                            resize(area[1] + area[3] / 2, "y")
                            - text_surface.get_height() / 2,
                        ),
                    )

                    pygame.draw.rect(
                        self.surface,
                        get_team_color(team),
                        (
                            resize(area[0], "x"),
                            resize(area[1], "y"),
                            resize(area[2], "x"),
                            resize(area[3], "y"),
                        ),
                        max(1, int(resize(4, "x"))),
                    )

            # Players
            for id, area in self.player_areas.items():
                draw_player_x, draw_player_y = area[0], area[1]
                if id == self.grab_player_id:
                    draw_player_x = self.mouse_x - area[2] / 2
                    draw_player_y = self.mouse_y - area[3] / 2

                # Team circle
                pygame.draw.circle(
                    self.surface,
                    get_team_color(self.players[id].team),
                    (
                        resize(draw_player_x + area[3] / 2, "x"),
                        resize(draw_player_y + area[3] / 2, "y"),
                    ),
                    int(resize(area[3] / 3, "x")),
                )
                if self.players[id].team == Team.NONE:
                    pygame.draw.circle(
                        self.surface,
                        (0, 0, 0),
                        (
                            resize(draw_player_x + area[3] / 2, "x"),
                            resize(draw_player_y + area[3] / 2, "y"),
                        ),
                        max(1, int(resize(area[3] / 6, "x"))),
                    )

                # Name
                text_surface = self.text.get_surface(
                    self.players[id].name,
                    30,
                    (255, 255, 255),
                )
                self.surface.blit(
                    text_surface,
                    (
                        resize(draw_player_x + area[2], "x") - text_surface.get_width(),
                        resize(draw_player_y + area[3] / 2, "y")
                        - text_surface.get_height() / 2,
                    ),
                )

                if self.is_hovered((draw_player_x, draw_player_y, area[2], area[3])):
                    color = (128, 128, 128)
                    for team, team_area in self.team_areas.items():
                        if self.is_hovered(team_area):
                            color = get_team_color(team)
                            break
                    pygame.draw.rect(
                        self.surface,
                        color,
                        (
                            resize(draw_player_x - 4, "x"),
                            resize(draw_player_y - 4, "y"),
                            resize(area[2] + 8, "x"),
                            resize(area[3] + 8, "y"),
                        ),
                        int(resize(4, "x")),
                    )

        # Player count
        text_surface = self.text.get_surface(
            f"{self.language.get(LanguageKey.MENU_SELECTION_PLAYER_COUNT)} {self.player_count}",
            40,
            (192, 192, 192),
        )
        self.surface.blit(
            text_surface,
            (
                resize(960, "x") - text_surface.get_width() / 2,
                resize(540 + self.menu_box_height / 2 - self.border_margin, "y")
                - text_surface.get_height(),
            ),
        )

        super().render()
