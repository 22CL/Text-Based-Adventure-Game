from typing import Final
from random import choice

from src.entities.BasicSpider import BasicSpider
from src.entities.BigSpider import BigSpider
from src.entities.Entity import Entity
from src.items.items import Item, Sword, Key


class Room:
    def __init__(self, coordinates: tuple[int, int], name: str, items: list[Item], enemies: list) -> None:
        self.__coordinates: Final[tuple[int, int]] = coordinates
        self.__name: str = name
        self.items: list[Item] = items
        self.enemies: list[Entity] = enemies
    
    def __repr__(self) -> str:
        return f"{self.__name}: {self.__coordinates}"


def setup_room(rooms: list[list[Room]], x: int, y: int, name: str, items: list[Item] = [], enemies: list[Entity] = []) -> None:
    rooms[x][y] = Room((x, y), name, items, enemies)

def setup_rooms(rooms: list[list[Room]]) -> None:
    setup_room(rooms, 1, 3, "Entrance")
    setup_room(rooms, 2, 3, "Combat Cave", enemies=[BasicSpider()])
    setup_room(rooms, 3, 3, "Rest")
    # Split
    # Up
    setup_room(rooms, 3, 2, "Locked door")
    setup_room(rooms, 4, 2, "Higher")
    setup_room(rooms, 5, 2, "Exit")

    # Down
    setup_room(rooms, 3, 4, "Chest room", items=[Sword("Strong Sword", 15)])
    setup_room(rooms, 4, 4, "Big Spider Fight", enemies=[BigSpider()])

    # Randomizer
    randomRooms = [(5, 4), (4, 5)]
    keyRoom = choice(randomRooms)
    randomRooms.remove(keyRoom)
    setup_room(rooms, keyRoom[0], keyRoom[1], "Key Room", items=[Key("Locked door key")])
    setup_room(rooms, randomRooms[0][0], randomRooms[0][1], "Trap Room", enemies=[BigSpider()])
