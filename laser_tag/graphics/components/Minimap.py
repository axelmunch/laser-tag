from math import ceil

import pygame

from ...configuration import VARIABLES
from ...entities.GameEntity import GameEntity
from ...game.Ray import Ray
from ...math.Line import Line
from ...math.rotations import rotate
from ..resize import resize
from .Component import Component


class Minimap(Component):
    """Minimap component"""

    def __init__(
        self, data={"map": [], "map_bounds": (0, 0, 1, 1), "entities": [], "rays": []}
    ):
        super().__init__()

        self.set_original_size(400, 400)

        self.update(data["map"], data["map_bounds"], data["entities"], data["rays"])

    def update(
        self,
        map: list[Line],
        map_bounds: tuple[int, int, int, int],
        entities: list[GameEntity],
        rays: list[Ray] = [],
    ):
        """
        Update the component

        Parameters:
            map (list): Map of the level
            map_bounds (int, int, int, int): Bounds of the map (min_x, min_y, max_x, max_y)
            entities (list): List of entities in the world
            rays (list): List of rays to render (optional)
        """
        self.data = {
            "map": map,
            "map_bounds": map_bounds,
            "entities": entities,
            "rays": rays,
        }
        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        map_width = ceil(self.data["map_bounds"][2] - self.data["map_bounds"][0])
        map_height = ceil(self.data["map_bounds"][3] - self.data["map_bounds"][1])
        for line in self.data["map"]:
            pygame.draw.line(
                self.surface,
                (0, 255, 255),
                (
                    (line.point1.x - self.data["map_bounds"][0])
                    * self.width
                    / map_width,
                    (line.point1.y - self.data["map_bounds"][1])
                    * self.height
                    / map_height,
                ),
                (
                    (line.point2.x - self.data["map_bounds"][0])
                    * self.width
                    / map_width,
                    (line.point2.y - self.data["map_bounds"][1])
                    * self.height
                    / map_height,
                ),
                max(1, int(resize(2))),
            )

        if VARIABLES.show_rays_minimap:
            for ray in self.data["rays"]:
                if ray.hit_point is not None:
                    pygame.draw.line(
                        self.surface,
                        (255, 255, 0),
                        (
                            (ray.origin.x - self.data["map_bounds"][0])
                            * self.width
                            / map_width,
                            (ray.origin.y - self.data["map_bounds"][1])
                            * self.height
                            / map_height,
                        ),
                        (
                            (ray.hit_point.x - self.data["map_bounds"][0])
                            * self.width
                            / map_width,
                            (ray.hit_point.y - self.data["map_bounds"][1])
                            * self.height
                            / map_height,
                        ),
                        max(1, int(resize(3))),
                    )

        for entity in self.data["entities"]:
            pygame.draw.circle(
                self.surface,
                (0, 128, 192),
                (
                    (entity.position.x - self.data["map_bounds"][0])
                    * self.width
                    / map_width,
                    (entity.position.y - self.data["map_bounds"][1])
                    * self.height
                    / map_height,
                ),
                ceil(entity.collider.radius * self.width / map_width),
            )

            facing_direction_position = rotate(0.5, entity.rotation, entity.position)
            pygame.draw.line(
                self.surface,
                (255, 255, 255),
                (
                    (entity.position.x - self.data["map_bounds"][0])
                    * self.width
                    / map_width,
                    (entity.position.y - self.data["map_bounds"][1])
                    * self.height
                    / map_height,
                ),
                (
                    (facing_direction_position.x - self.data["map_bounds"][0])
                    * self.width
                    / map_width,
                    (facing_direction_position.y - self.data["map_bounds"][1])
                    * self.height
                    / map_height,
                ),
                max(1, int(resize(3))),
            )

        super().render()
