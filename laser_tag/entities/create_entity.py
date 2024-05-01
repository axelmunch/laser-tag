from .BarrelShort import BarrelShort
from .BarrelTall import BarrelTall
from .Entity import Entity
from .GameEntity import GameEntity
from .LaserRay import LaserRay
from .Player import Player


def create_entity(parsed_object: list):
    try:
        entity_object = parsed_object[1:]
        match parsed_object[0]:
            case Entity.__name__:
                return Entity.create(entity_object)
            case GameEntity.__name__:
                return GameEntity.create(entity_object)
            case Player.__name__:
                return Player.create(entity_object)
            case LaserRay.__name__:
                return LaserRay.create(entity_object)
            case BarrelShort.__name__:
                return BarrelShort.create(entity_object)
            case BarrelTall.__name__:
                return BarrelTall.create(entity_object)
    except:
        pass

    return None
