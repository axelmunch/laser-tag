class Variables:
    def __init__(self):
        # Default values
        self.full_screen_width = 1920
        self.full_screen_height = 1080
        self.screen_width = 1280
        self.screen_height = 720
        self.fullscreen = False

        self.server_port = 16168

        self.fps = 60

        self.show_fps = True
        self.show_network_stats = True

        self.debug = True

        self.rotate_sensitivity = 3

        self.pseudo = "Player"

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
