from __future__ import annotations

from ..game.Team import Team
from ..math.Line import Line
from ..math.Point import Point
from .GameEntity import GameEntity


class LaserRay(GameEntity):
    """Laser ray entity"""

    def __init__(self, position: Point, end_position: Point, parent_id=None):
        super().__init__(position, LaserRay.entity_radius())

        self.move_speed = 0
        self.attack_speed = 0
        self.can_be_attacked = False

        self.end_position = end_position
        self.parent_id = parent_id
        self.get_entity_fct = None
        self.time_to_live = 0.1

        self.ray = Line(self.position, self.end_position)

    def __repr__(self):
        return f"['{self.__class__.__name__}',{self.position},{self.end_position},{self.parent_id},{self.rotation},{self.team},{self.damages},{self.score},{self.eliminations},{self.time_to_live},{int(self.can_attack)}]"

    @staticmethod
    def create(parsed_object) -> LaserRay:
        try:
            position = Point.create(parsed_object[0])
            end_position = Point.create(parsed_object[1])
            if position is None or end_position is None:
                return None

            entity = LaserRay(position, end_position, parsed_object[2])
            entity.rotation = float(parsed_object[3])
            entity.team = Team(parsed_object[4])
            entity.damages = int(parsed_object[5])
            entity.score = float(parsed_object[6])
            entity.eliminations = int(parsed_object[7])
            entity.time_to_live = float(parsed_object[8])
            entity.can_attack = bool(parsed_object[9])
            return entity
        except:
            return None

    @staticmethod
    def entity_radius() -> float:
        return 0

    def on_hit(self, entity: GameEntity):
        super().on_hit(entity)
        self.death()

    def on_kill(self, entity: GameEntity):
        super().on_kill(entity)
        self.give_stats_to_parent()

    def death(self):
        super().death()
        self.give_stats_to_parent()

    def attack(self) -> bool:
        return self.can_attack

    def give_stats_to_parent(self):
        if self.get_entity_fct is not None and (
            self.eliminations > 0 or self.score > 0
        ):
            parent = self.get_entity_fct(self.parent_id)
            if parent is not None:
                # Add eliminations to parent
                parent.eliminations += self.eliminations
                self.eliminations = 0
                # Add score to parent
                parent.score += self.score
                self.score = 0

    def collides_with(self, other: GameEntity) -> bool:
        return other.collider.collides_with_segment(self.ray)
