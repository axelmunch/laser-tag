class Variables:
    def __init__(self):
        # Default values
        self.full_screen_width = 0
        self.full_screen_height = 0
        self.screen_width = self.full_screen_width
        self.screen_height = self.full_screen_height
        self.fullscreen = False

        self.server_port = 16168

        self.fps = 60

        self.show_fps = True
        self.show_network_stats = True
        self.show_components_outline = False
        self.show_rays_minimap = False

        self.level_editor = False

        self.anti_aliased_text = True

        self.debug = True

        self.rotate_sensitivity = 5 / 100

        self.pseudo = "Player"

        self.fov = 80
        self.ray_width = 15
        self.rays_quantity = 1920 // self.ray_width
        self.wall_height_approximation = 1920 // self.rays_quantity
        self.world_scale = 1200

        self.assets_folder = "default"

        # Load from file
        self.load()

    def load(self):
        pass

    def set_full_screen_size(self, width, height):
        self.full_screen_width = width
        self.full_screen_height = height

    def set_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
