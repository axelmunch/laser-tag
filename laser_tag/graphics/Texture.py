import pygame

from ..configuration import DEFAULT_TEXTURE_CACHE_LIMIT, MASK_COLOR, VARIABLES
from ..game.Team import Team, get_team_color
from .resize import resize


class Texture:
    """Texture class that manages surfaces and caching"""

    def __init__(self, path, alpha: bool = False, custom_size: tuple[int, int] = None):
        self.texture_cache = {}

        self.cache_limit = DEFAULT_TEXTURE_CACHE_LIMIT

        try:
            texture = pygame.image.load(path)
        except FileNotFoundError:
            if VARIABLES.debug:
                print(f"Texture not found: {path}")
            texture = pygame.Surface((16, 16))
            texture.fill(MASK_COLOR)
            pygame.draw.circle(texture, (0, 0, 0), (8, 8), 4)

        if alpha:
            texture = texture.convert_alpha()
        else:
            texture = texture.convert()

        if custom_size:
            texture = pygame.transform.scale(texture, custom_size)

        self.original_width, self.original_height = texture.get_size()

        self.origial_surfaces = {None: texture}

        self.resize()

    def resize(
        self, size: tuple[float, float] = None, team: Team = None
    ) -> pygame.Surface:
        if size is None:
            size = (self.original_width, self.original_height, team)

        size = (int(resize(size[0], "x")), int(resize(size[1], "y")), team)

        if size not in self.texture_cache:
            self.texture_cache[size] = pygame.transform.scale(
                self.get_original_surface(team), (size[0], size[1])
            )

            self.reduce_cache()

        return self.texture_cache[size]

    def get_surface(self, team: Team = None) -> pygame.Surface:
        return self.resize(team=team)

    def get_original_surface(self, team: Team = None) -> pygame.Surface:
        if team not in self.origial_surfaces:
            self.origial_surfaces[team] = self.origial_surfaces[None].copy()
            self.mask_surface_team_color(self.origial_surfaces[team], team)

        return self.origial_surfaces[team]

    def get_original_size(self) -> tuple[int, int]:
        return self.original_width, self.original_height

    def reduce_cache(self):
        if len(self.texture_cache) > self.cache_limit:
            self.texture_cache = dict(
                list(self.texture_cache.items())[-self.cache_limit :]
            )

    def clear_cache(self):
        self.texture_cache.clear()

    def set_cache_limit(self, limit: int):
        self.cache_limit = limit
        self.reduce_cache()

    def mask_surface_team_color(
        self, surface: pygame.Surface, team: Team
    ) -> pygame.Surface:
        team_color = get_team_color(team)

        mask_color = MASK_COLOR

        mask = pygame.mask.from_threshold(surface, mask_color, (1, 1, 1))

        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if mask.get_at((x, y)):
                    surface.set_at((x, y), team_color)
