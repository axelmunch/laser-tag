from .BarrelShort import BarrelShort
from .BarrelTall import BarrelTall
from .Entity import Entity
from .GameEntity import GameEntity
from .Player import Player
from .Projectile import Projectile


def create_entity(parsed_object: list):
    try:
        entity_object = parsed_object[1:]
        match parsed_object[0]:
            case "Entity":
                return Entity.create(entity_object)
            case "GameEntity":
                return GameEntity.create(entity_object)
            case "Player":
                return Player.create(entity_object)
            case "Projectile":
                return Projectile.create(entity_object)
            case "BarrelShort":
                return BarrelShort.create(entity_object)
            case "BarrelTall":
                return BarrelTall.create(entity_object)
    except:
        pass

    return None
