import json
from typing import TypedDict

from ..entities.create_entity import create_entity
from ..entities.Entity import Entity
from ..math.Point import Point
from ..network.safe_eval import safe_eval
from .Wall import Wall


class MapData(TypedDict):
    walls: list[Wall]
    entities: list[Entity]
    spawn_points: list[Point]


def load_world(map_file):
    map_data: MapData = {"walls": [], "entities": [], "spawn_points": []}
    read_data = {}
    try:
        with open(map_file, "r") as file:
            read_data: MapData = json.load(file)
    except FileNotFoundError:
        read_data: MapData = {"walls": [], "entities": [], "spawn_points": []}

    for wall in read_data["walls"]:
        element = Wall.create(safe_eval(wall))
        if element is not None:
            map_data["walls"].append(element)
    for entity in read_data["entities"]:
        element = create_entity(safe_eval(entity))
        if element is not None:
            map_data["entities"].append(element)
    for spawn_point in read_data["spawn_points"]:
        element = Point.create(safe_eval(spawn_point))
        if element is not None:
            map_data["spawn_points"].append(element)

    return map_data
