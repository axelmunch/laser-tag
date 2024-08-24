from math import ceil, cos
from time import time

import pygame

from ...configuration import ENTITIES_ROTATION_FRAMES, MAX_WALL_HEIGHT, VARIABLES
from ...entities.GameEntity import GameEntity
from ...entities.LaserRay import LaserRay
from ...entities.Player import Player
from ...game.Ray import Ray
from ...game.Team import get_team_color
from ...game.Wall import WallType
from ...math.degrees_radians import degrees_to_radians
from ...math.distance import distance_points
from ...math.Point import Point
from ...math.rotations import get_angle
from ..AssetsLoader import TextureNames
from ..resize import resize
from ..Textures import Textures
from .Component import Component
from .Crosshair import Crosshair
from .HUD import HUD

textures = Textures()


class World(Component):
    """World component"""

    def __init__(
        self,
        data={"rays": [], "entities": [], "current_entity": None},
    ):
        super().__init__()

        self.set_original_size(1920, 1080)

        self.crosshair = Crosshair()
        self.hud = HUD()

        self.update(data["rays"], data["entities"], data["current_entity"])

    def resize(self):
        super().resize()

        try:
            self.crosshair.resize()
            self.hud.resize()
        except AttributeError:
            pass

    def update(
        self,
        rays: list[tuple[int, Ray]],
        entities: list[GameEntity],
        current_entity: GameEntity = None,
    ):
        """
        Update the component

        Parameters:
            rays (list): List of rays to render
            entities (list): List of entities in the world
            current_entity (GameEntity): The current entity
        """

        self.data = {
            "rays": rays,
            "entities": entities,
            "current_entity": current_entity,
        }

        self.crosshair.update()

        if current_entity is not None and isinstance(current_entity, Player):
            self.hud.update(
                current_entity.deactivation_time_ratio, current_entity.can_attack
            )

        super().update()

    def position_to_screen(self, point: Point) -> float:
        # In view if value between 0 and 1

        angle_with_current_entity = (
            get_angle(point, center=self.data["current_entity"].position)
            - self.data["current_entity"].rotation
            + 180
        ) % 360 - 180

        return 0.5 + angle_with_current_entity / VARIABLES.fov

    def render(self):
        self.surface.fill((42, 42, 42))
        # Sky
        pygame.draw.rect(
            self.surface, (64, 64, 64), (0, 0, resize(1920, "x"), resize(540, "y")), 0
        )

        render_list = RenderList()

        # List rays
        if len(self.data["rays"]) > 0:
            for i, ray in self.data["rays"]:
                if ray.hit_point is not None:
                    render_list.add(i * VARIABLES.ray_width, ray.distance, ray)

        # List entities
        for entity in self.data["entities"]:
            if self.data["current_entity"] is None:
                break

            distance = distance_points(
                self.data["current_entity"].position, entity.position
            )

            if distance > 0:
                x_position = self.position_to_screen(entity.position)
                margin = 5
                if (
                    x_position is not None
                    and x_position * 100 > -margin
                    and x_position * 100 < 100 + margin
                ):
                    render_list.add(x_position, distance, entity)

        render_queue = render_list.get()

        for element in render_queue:
            x_position = element["x_position"]
            distance = element["distance"]
            object = element["object"]

            if isinstance(object, Ray):
                ray = object

                ray_world_size = 0
                if ray.distance != 0:
                    if self.data["current_entity"] is not None:
                        # Fix fisheye effect
                        ray_world_size = VARIABLES.world_scale / (
                            ray.distance
                            * cos(
                                degrees_to_radians(
                                    (
                                        self.data["current_entity"].rotation
                                        - ray.direction
                                    )
                                )
                            )
                        )
                    else:
                        ray_world_size = VARIABLES.world_scale / ray.distance

                # Limit wall height
                ray_world_size = min(ray_world_size, MAX_WALL_HEIGHT)

                approximate_display_size = ray_world_size

                ratio = ray.hit_infos["line_intersecting"].get_point_ratio_on_line(
                    ray.hit_infos["intersection_point"]
                )
                line_rotation = ray.hit_infos["line_intersecting"].get_rotation()

                reversed_texture = False

                if self.data["current_entity"] is not None:
                    rotation = self.data["current_entity"].rotation

                    rotation_difference = abs(line_rotation - rotation + 90)
                    if rotation_difference <= 90 or rotation_difference >= 270:
                        reversed_texture = True

                texture_name = TextureNames.BLUE
                match ray.hit_infos["wall_type"]:
                    case WallType.WALL_1:
                        texture_name = TextureNames.BLUE
                    case WallType.WALL_2:
                        texture_name = TextureNames.RED
                    case WallType.WALL_3:
                        texture_name = TextureNames.GREEN
                    case WallType.WALL_4:
                        texture_name = TextureNames.BLUE
                texture_surface_full = textures.get_original_surface(texture_name)

                texture_size_ratio = (
                    texture_surface_full.get_height() / approximate_display_size
                )
                resized_ray_width = ceil(VARIABLES.ray_width * texture_size_ratio)

                # Crop surface to the center
                height_cropping_offset = 0
                if approximate_display_size > 1080:
                    height_cropping_offset = int(
                        resize(
                            (approximate_display_size - 1080) / 2,
                            "y",
                        )
                        * texture_size_ratio
                    )

                subsurface_start = texture_surface_full.get_width() * ratio
                if (
                    subsurface_start + resized_ray_width
                    > texture_surface_full.get_width()
                ):
                    subsurface_start = max(
                        0, texture_surface_full.get_width() - resized_ray_width
                    )

                texture_subsurface = texture_surface_full.subsurface(
                    (
                        subsurface_start,
                        height_cropping_offset,
                        min(
                            resized_ray_width,
                            texture_surface_full.get_width() - subsurface_start,
                        ),
                        texture_surface_full.get_height() - height_cropping_offset * 2,
                    )
                )

                texture_subsurface = pygame.transform.scale(
                    texture_subsurface,
                    (
                        ceil(resize(VARIABLES.ray_width, "x")),
                        resize(approximate_display_size, "y"),
                    ),
                )
                if reversed_texture:
                    texture_subsurface = pygame.transform.flip(
                        texture_subsurface, True, False
                    )

                self.surface.blit(
                    texture_subsurface,
                    (
                        resize(x_position, "x"),
                        resize(540, "y") - texture_subsurface.get_height() / 2,
                    ),
                )

                # Darkening effect
                darkness_value = min(255, ray.distance * 20)
                dark_mask = pygame.Surface(
                    texture_subsurface.get_size(), pygame.SRCALPHA
                )
                dark_mask.fill((0, 0, 0, darkness_value))

                self.surface.blit(
                    dark_mask,
                    (
                        resize(x_position, "x"),
                        resize(540, "y") - dark_mask.get_height() / 2,
                    ),
                )

            elif isinstance(object, Player):
                angle = 0
                if self.data["current_entity"] is not None:
                    angle = (
                        get_angle(
                            object.position, center=self.data["current_entity"].position
                        )
                        - object.rotation
                        + 180
                        + 180 / ENTITIES_ROTATION_FRAMES
                    ) % 360

                rotation_frame = int(angle / 360 * ENTITIES_ROTATION_FRAMES)

                texture = TextureNames.GREEN

                entity_world_size = min(VARIABLES.world_scale / distance, 1080)

                texture_original_size = textures.get_original_size(texture)
                texture_scale_ratio = entity_world_size / texture_original_size[1] * 0.7
                texture_new_size = (
                    texture_original_size[0] * texture_scale_ratio,
                    texture_original_size[1] * texture_scale_ratio,
                )

                # Display the entity
                self.surface.blit(
                    textures.resize_texture(
                        texture, (texture_new_size[0], texture_new_size[1])
                    ),
                    (
                        resize(x_position * 1920 - texture_new_size[0] / 2, "x"),
                        resize(540 + entity_world_size / 2 - texture_new_size[1], "y"),
                    ),
                )

                # Display a text with the name
                text_distance = max(1, distance)
                text_margin = 10
                text_surface = self.text.get_surface(
                    object.name, 125 / text_distance, get_team_color(object.team)
                )
                self.surface.blit(
                    text_surface,
                    (
                        resize(x_position * 1920, "x") - text_surface.get_width() / 2,
                        max(
                            resize(text_margin, "y"),
                            resize(
                                540
                                + entity_world_size / 2
                                - texture_new_size[1]
                                - text_margin / text_distance,
                                "y",
                            )
                            - text_surface.get_height(),
                        ),
                    ),
                )

            elif isinstance(object, GameEntity):
                texture = TextureNames.RED

                entity_world_size = min(VARIABLES.world_scale / distance, 1080)

                if isinstance(object, LaserRay):
                    texture = TextureNames.RED
                    entity_world_size *= 0.5

                texture_original_size = textures.get_original_size(texture)
                texture_scale_ratio = entity_world_size / texture_original_size[1] * 0.7
                texture_new_size = (
                    texture_original_size[0] * texture_scale_ratio,
                    texture_original_size[1] * texture_scale_ratio,
                )

                # Display the entity
                self.surface.blit(
                    textures.resize_texture(
                        texture, (texture_new_size[0], texture_new_size[1])
                    ),
                    (
                        resize(x_position * 1920 - texture_new_size[0] / 2, "x"),
                        resize(540 + entity_world_size / 2 - texture_new_size[1], "y"),
                    ),
                )

        # Crosshair
        self.surface.blit(
            self.crosshair.get(),
            (
                resize(960, "x") - self.crosshair.get().get_width() / 2,
                resize(540, "y") - self.crosshair.get().get_height() / 2,
            ),
        )

        # HUD
        self.surface.blit(
            self.hud.get(), (0, resize(1080, "y") - self.hud.get().get_height())
        )

        super().render()


class RenderList:
    """Render list to order elements by distance"""

    def __init__(self):
        self.list: list[dict[float, float, Ray | GameEntity]] = []

    def add(self, x_position: float, distance: float, object: Ray | GameEntity):
        self.list.append(
            {"x_position": x_position, "distance": distance, "object": object}
        )

    def sort(self):
        # Sort by greatest distance
        self.list.sort(key=lambda x: x["distance"], reverse=True)

    def get(self):
        self.sort()
        return self.list
