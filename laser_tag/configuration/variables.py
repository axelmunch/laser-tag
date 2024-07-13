import json


class Variables:
    def __init__(self, version, settings_file):
        self.version = version
        self.settings_file = settings_file
        self.variables_save_exclusion = [
            "settings_file",
            "variables_save_exclusion",
            "full_screen_width",
            "full_screen_height",
            "screen_width",
            "screen_height",
            "resize_display",
        ]

        # Default values
        self.full_screen_width = 0
        self.full_screen_height = 0
        self.screen_width = self.full_screen_width
        self.screen_height = self.full_screen_height
        self.fullscreen = False
        self.windowed_resolution_ratio = 0.5
        self.resize_display = False

        self.server_port = 16168

        self.fps = 60

        self.show_fps = True
        self.show_network_stats = True
        self.show_components_outline = False
        self.show_rays_minimap = False
        self.show_minimap = True
        self.show_all_entities_minimap = False

        self.level_editor = False

        self.anti_aliased_text = True

        self.debug = False

        self.rotate_sensitivity = 5 / 100

        self.player_name = "Player"

        self.fov = 80
        self.ray_width = 15
        self.rays_quantity = 1920 // self.ray_width
        self.wall_height_approximation = 1920 // self.rays_quantity
        self.world_scale = 1200

        self.assets_folder = "default"
        self.language = "EN"

        # Load from file
        self.load()

    def load(self):
        try:
            with open(self.settings_file, "r", encoding="utf-8") as file:
                variables = json.load(file)
                current_version = self.version
                self.__dict__.update(variables)
                if "version" not in variables or self.version != current_version:
                    self.version = current_version
                    if self.debug:
                        print("Variables version update")
                    self.save()
        except FileNotFoundError:
            self.save()

        if self.debug:
            print("Variables loaded")

    def save(self):
        variables = {
            key: value
            for key, value in self.__dict__.items()
            if key not in self.variables_save_exclusion
        }

        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.settings_file, "w") as file:
            json.dump(variables, file, indent=4)
            file.write("\n")

        if self.debug:
            print("Variables saved")

    def set_full_screen_size(self, width, height):
        self.full_screen_width = width
        self.full_screen_height = height

    def set_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
