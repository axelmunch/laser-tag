import pygame

from ....configuration import VARIABLES
from ....events.EventInstance import EventInstance
from ....language.LanguageKey import LanguageKey
from ...AssetsLoader import get_assets_folders, load_assets, open_assets_folder
from ...resize import resize
from ..Component import Component
from ..GraphicalButton import ButtonType, GraphicalButton
from ..GraphicalCheckbox import GraphicalCheckbox
from ..GraphicalComboBox import GraphicalComboBox
from ..GraphicalNumberSelect import GraphicalNumberSelect
from ..GraphicalSlider import GraphicalSlider
from ..GraphicalText import GraphicalText
from .Menu import Menu


class SettingsMenu(Component, Menu):
    """Settings menu component"""

    def __init__(self):
        Component.__init__(self)
        Menu.__init__(self)

        self.set_original_size(1920, 1080)

        self.settings_box_width = 1920 - 500
        self.settings_box_height = 1080 - 200
        border_margin = 50
        button_width = (self.settings_box_width - 20 * 5 - border_margin * 2) / 5
        button_height = 100

        self.back_button = GraphicalButton(
            960 - self.settings_box_width / 2 + 50,
            540 + self.settings_box_height / 2 - button_height * 1.5,
            button_width,
            button_height,
            text_key=LanguageKey.MENU_SETTINGS_BACK,
            action=lambda: self.set_active(False),
        )
        self.default_elements = [self.back_button]

        self.pages_buttons = [
            GraphicalButton(
                960
                - self.settings_box_width / 2
                + border_margin
                + 20 * 0
                + button_width * 0,
                540 - self.settings_box_height / 2 + border_margin,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_GENERAL,
                action=lambda: self.switch_settings_page(0),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
            GraphicalButton(
                960
                - self.settings_box_width / 2
                + border_margin
                + 20 * 1
                + button_width * 1,
                540 - self.settings_box_height / 2 + border_margin,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_DISPLAY,
                action=lambda: self.switch_settings_page(1),
                type=ButtonType.SETTINGS_CATEGORY,
            ),
            # GraphicalButton(
            #     960
            #     - self.settings_box_width / 2
            #     + border_margin
            #     + 20 * 2
            #     + button_width * 2,
            #     540 - self.settings_box_height / 2 + border_margin,
            #     button_width,
            #     button_height,
            #     text_key=LanguageKey.MENU_SETTINGS_CONTROLS,
            #     action=lambda: self.switch_settings_page(2),
            #     type=ButtonType.SETTINGS_CATEGORY,
            # ),
            # GraphicalButton(
            #     960
            #     - self.settings_box_width / 2
            #     + border_margin
            #     + 20 * 3
            #     + button_width * 3,
            #     540 - self.settings_box_height / 2 + border_margin,
            #     button_width,
            #     button_height,
            #     text_key=LanguageKey.MENU_SETTINGS_AUDIO,
            #     action=lambda: self.switch_settings_page(3),
            #     type=ButtonType.SETTINGS_CATEGORY,
            # ),
            GraphicalButton(
                960
                - self.settings_box_width / 2
                + border_margin
                + 20 * 4
                + button_width * 4,
                540 - self.settings_box_height / 2 + border_margin,
                button_width,
                button_height,
                text_key=LanguageKey.MENU_SETTINGS_DEBUG,
                action=lambda: self.switch_settings_page(2),
                type=ButtonType.SETTINGS_CATEGORY,
                disabled=not VARIABLES.debug,
            ),
        ]
        self.pages_elements = [
            [
                GraphicalText(
                    960 - self.settings_box_width / 4 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 150 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_FOV),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalSlider(
                    960 - self.settings_box_width / 4,
                    540 - self.settings_box_height / 2 + border_margin + 150,
                    60,
                    110,
                    VARIABLES.fov,
                    0,
                    change_action=lambda i: setattr(VARIABLES, "fov", i),
                ),
                GraphicalText(
                    960 - self.settings_box_width / 4 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 300 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_RAY_WIDTH),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalNumberSelect(
                    960 - self.settings_box_width / 4,
                    540 - self.settings_box_height / 2 + border_margin + 300,
                    1,
                    32,
                    VARIABLES.ray_width,
                    change_action=self.change_ray_width,
                ),
                GraphicalText(
                    960 - self.settings_box_width / 4 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 450 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_LANGUAGE),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalComboBox(
                    960 - self.settings_box_width / 4,
                    540 - self.settings_box_height / 2 + border_margin + 450,
                    choices=self.language.get_language_list(),
                    default_choice=VARIABLES.language,
                    change_action=lambda i: self.change_language(i),
                    disabled=False,
                    selected=False,
                ),
                GraphicalText(
                    960 + self.settings_box_width / 6 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 450 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_ASSETS_PACK),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalComboBox(
                    960 + self.settings_box_width / 6,
                    540 - self.settings_box_height / 2 + border_margin + 450,
                    choices={name: name for name in get_assets_folders()},
                    default_choice=VARIABLES.assets_folder,
                    change_action=lambda i: self.change_assets(i),
                    disabled=False,
                    selected=False,
                ),
                GraphicalButton(
                    960 + self.settings_box_width / 6 + 270,
                    540 - self.settings_box_height / 2 + border_margin + 450,
                    button_height,
                    button_height,
                    action=open_assets_folder,
                    type=ButtonType.OPEN_FOLDER,
                ),
            ],
            [
                GraphicalText(
                    960 - self.settings_box_width / 4 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 150 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_SHOW_FPS),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalCheckbox(
                    960 - self.settings_box_width / 4,
                    540 - self.settings_box_height / 2 + border_margin + 150 + 25,
                    VARIABLES.show_fps,
                    check_action=lambda: setattr(VARIABLES, "show_fps", True),
                    uncheck_action=lambda: setattr(VARIABLES, "show_fps", False),
                    disabled=False,
                    selected=False,
                ),
                GraphicalText(
                    960 + self.settings_box_width / 6 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 150 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_FPS),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalComboBox(
                    960 + self.settings_box_width / 6,
                    540 - self.settings_box_height / 2 + border_margin + 150,
                    choices={
                        0: 0,
                        25: 25,
                        60: 60,
                        120: 120,
                        144: 144,
                        150: 150,
                        240: 240,
                    },
                    default_choice=VARIABLES.fps,
                    change_action=lambda i: setattr(VARIABLES, "fps", i),
                    disabled=False,
                    selected=False,
                ),
                GraphicalText(
                    960 - self.settings_box_width / 4 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 300 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(
                        LanguageKey.MENU_SETTINGS_TEXT_ANTI_ALIASING
                    ),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalCheckbox(
                    960 - self.settings_box_width / 4,
                    540 - self.settings_box_height / 2 + border_margin + 300 + 25,
                    VARIABLES.anti_aliased_text,
                    check_action=lambda: setattr(VARIABLES, "anti_aliased_text", True),
                    uncheck_action=lambda: setattr(
                        VARIABLES, "anti_aliased_text", False
                    ),
                    disabled=False,
                    selected=False,
                ),
                GraphicalText(
                    960 - self.settings_box_width / 4 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 450 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_RESOLUTION),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalSlider(
                    960 - self.settings_box_width / 4,
                    540 - self.settings_box_height / 2 + border_margin + 450,
                    0.2,
                    1,
                    VARIABLES.windowed_resolution_ratio,
                    1,
                    change_action=lambda i: self.change_screen_resolution(i),
                ),
                GraphicalText(
                    960 + self.settings_box_width / 6 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 450 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_FULLSCREEN),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalCheckbox(
                    960 + self.settings_box_width / 6,
                    540 - self.settings_box_height / 2 + border_margin + 450 + 25,
                    VARIABLES.fullscreen,
                    check_action=lambda: self.change_fullscreen(True),
                    uncheck_action=lambda: self.change_fullscreen(False),
                    disabled=False,
                    selected=False,
                ),
            ],
            # [],
            # [],
            [
                GraphicalText(
                    960 - self.settings_box_width / 4 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 150 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_NETWORK_STATS),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalCheckbox(
                    960 - self.settings_box_width / 4,
                    540 - self.settings_box_height / 2 + border_margin + 150 + 25,
                    VARIABLES.show_network_stats,
                    check_action=lambda: setattr(VARIABLES, "show_network_stats", True),
                    uncheck_action=lambda: setattr(
                        VARIABLES, "show_network_stats", False
                    ),
                    disabled=False,
                    selected=False,
                ),
                GraphicalText(
                    960 + self.settings_box_width / 6 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 150 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_COMPONENTS_OUTLINE),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalCheckbox(
                    960 + self.settings_box_width / 6,
                    540 - self.settings_box_height / 2 + border_margin + 150 + 25,
                    VARIABLES.show_components_outline,
                    check_action=lambda: setattr(
                        VARIABLES, "show_components_outline", True
                    ),
                    uncheck_action=lambda: setattr(
                        VARIABLES, "show_components_outline", False
                    ),
                    disabled=False,
                    selected=False,
                ),
                GraphicalText(
                    960 - self.settings_box_width / 4 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 300 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_RAYS_MINIMAP),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalCheckbox(
                    960 - self.settings_box_width / 4,
                    540 - self.settings_box_height / 2 + border_margin + 300 + 25,
                    VARIABLES.show_rays_minimap,
                    check_action=lambda: setattr(VARIABLES, "show_rays_minimap", True),
                    uncheck_action=lambda: setattr(
                        VARIABLES, "show_rays_minimap", False
                    ),
                    disabled=False,
                    selected=False,
                ),
                GraphicalText(
                    960 + self.settings_box_width / 6 - 20,
                    540 - self.settings_box_height / 2 + border_margin + 300 + 50,
                    align_x="right",
                    align_y="center",
                    text=self.language.get(LanguageKey.MENU_SETTINGS_ALL_ENTITIES_MINIMAP),
                    size=50,
                    color=(0, 0, 255),
                ),
                GraphicalCheckbox(
                    960 + self.settings_box_width / 6,
                    540 - self.settings_box_height / 2 + border_margin + 300 + 25,
                    VARIABLES.show_all_entities_minimap,
                    check_action=lambda: setattr(
                        VARIABLES, "show_all_entities_minimap", True
                    ),
                    uncheck_action=lambda: setattr(
                        VARIABLES, "show_all_entities_minimap", False
                    ),
                    disabled=False,
                    selected=False,
                ),
            ],
        ]
        self.elements = []

        self.switch_settings_page(0)

        self.update()

    def resize(self):
        super().resize()

        try:
            for element in self.elements:
                element.resize()
        except AttributeError:
            pass

    def change_screen_resolution(self, value):
        VARIABLES.windowed_resolution_ratio = value
        VARIABLES.resize_display = True

    def change_fullscreen(self, value):
        VARIABLES.fullscreen = value
        VARIABLES.resize_display = True

    def change_ray_width(self, value):
        VARIABLES.ray_width = value
        VARIABLES.rays_quantity = 1920 // VARIABLES.ray_width
        VARIABLES.wall_height_approximation = 1920 // VARIABLES.rays_quantity

    def change_assets(self, assets_folder):
        VARIABLES.assets_folder = assets_folder
        load_assets()

    def change_language(self, language):
        VARIABLES.language = language
        self.language.set_language(language)

    def switch_settings_page(self, page: int):
        # Default
        self.elements = self.default_elements[:]

        for i, element in enumerate(self.pages_buttons):
            element.set_selected(i == page)
            self.elements.append(element)

        for element in self.pages_elements[page]:
            self.elements.append(element)

    def set_active(self, active: bool):
        if not active:
            VARIABLES.save()
        return super().set_active(active)

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

        pygame.draw.rect(
            self.surface,
            (0, 100, 0),
            (
                resize(960 - self.settings_box_width / 2, "x"),
                resize(540 - self.settings_box_height / 2, "y"),
                resize(self.settings_box_width, "x"),
                resize(self.settings_box_height, "y"),
            ),
        )

        settings_title_text = self.text.get_surface(
            self.language.get(LanguageKey.MENU_SETTINGS_TITLE), 50, (255, 255, 255)
        )
        self.surface.blit(
            settings_title_text,
            (
                resize(960, "x") - settings_title_text.get_width() / 2,
                resize(540 - self.settings_box_height / 2 + 20, "y"),
            ),
        )

        for element in self.elements:
            self.surface.blit(
                element.get(), (resize(element.x, "x"), resize(element.y, "y"))
            )

        super().render()
