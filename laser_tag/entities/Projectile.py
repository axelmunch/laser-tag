from __future__ import annotations

from threading import Lock

from ..math.Point import Point
from .GameEntity import GameEntity


class Projectile(GameEntity):
    """Projectile entity"""

    def __init__(self, position: Point, parent_id=None):
        super().__init__(position, Projectile.entity_radius())

        self.move_speed = 0.2
        self.attack_speed = 0
        self.can_be_attacked = False

        self.parent_id = parent_id
        self.get_entity_fct = None
        self.give_stats_to_parent_mutex = Lock()

    def __repr__(self):
        return f"['{self.__class__.__name__}',{self.position},{self.rotation},{self.team},{self.damages},{self.score},{self.eliminations},{self.parent_id}]"

    @staticmethod
    def create(parsed_object) -> Projectile:
        try:
            position = Point.create(parsed_object[0])
            if position is None:
                return None

            entity = Projectile(position, parsed_object[6])
            entity.rotation = float(parsed_object[1])
            entity.team = int(parsed_object[2])
            entity.damages = int(parsed_object[3])
            entity.score = float(parsed_object[4])
            entity.eliminations = int(parsed_object[5])
            return entity
        except:
            return None

    @staticmethod
    def entity_radius() -> float:
        return 0.05

    def on_hit(self, entity: GameEntity):
        super().on_hit(entity)
        self.death()

    def on_kill(self, entity: GameEntity):
        super().on_kill(entity)
        self.give_stats_to_parent()

    def death(self):
        super().death()
        self.give_stats_to_parent()

    def give_stats_to_parent(self):
        self.give_stats_to_parent_mutex.acquire()
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
        self.give_stats_to_parent_mutex.release()
