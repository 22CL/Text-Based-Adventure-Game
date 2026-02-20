from typing import Final, Annotated, Optional
import random
import yaml
from os import path

from src.directions import Direction
from src.entities.Entity import Entity
from src.items.items import Item
from src.player import Player


class Room:
    def __init__(self,
                 position: Annotated[list[int], 2],
                 name: str,
                 items: list[Item] = None,
                 enemies: list[Entity] = None,
                 locked: bool = False,
                 requiredItemToOpenId: Optional[str] = None
                 ) -> None:
        if locked and requiredItemToOpenId is None:
            raise ValueError(f"requiredItemToOpenId must be provided when locked is True for {name} room")

        # noinspection PyTypeChecker
        self.position: Final[tuple[int, int]] = tuple(position)
        self.name: Final[str] = name
        self.items: list[Item] = items if items is not None else []
        self.enemies: list[Entity] = enemies if enemies is not None else []
        self.locked: bool = locked
        if self.locked:
            self.requiredItemToOpenId: Final[str] = requiredItemToOpenId

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.enemies is None:
            self.enemies = []

    def __repr__(self) -> str:
        if self.locked:
            return f"{self.name}: {self.position}, required item id: {self.requiredItemToOpenId}, enemies: {self.enemies}, items: {self.items}"
        else:
            return f"{self.name}: {self.position}, locked: {self.locked}, enemies: {self.enemies}, items: {self.items}"


def get_rooms() -> list[list[None | Room]]:
    return rooms2d


def get_room_at_player(player: Player, rooms: list[list[None | Room]]) -> Room:
    return rooms[player.get_position()[0]][player.get_position()[1]]


def get_next_room(player: Player, direction: Direction, rooms: list[list[None | Room]]) -> Room | None:
    return rooms[player.get_position()[0] + direction.value[0]][player.get_position()[1] + direction.value[1]]


with open(path.join("config", "rooms.yaml"), 'r', encoding="utf-8-sig") as file:
    data = yaml.safe_load(file)

roomsInfo = data['rooms']

rooms1d: list[Room] = []
flexible_groups: dict[str, list[dict]] = {}

for roomData in roomsInfo:
    position = roomData['position']
    if all(isinstance(p, list) for p in position):
        # Use the position pool as a hashable key to group rooms that share the same pool
        position_key = str(sorted([tuple(p) for p in position]))
        if position_key not in flexible_groups:
            flexible_groups[position_key] = []
        flexible_groups[position_key].append(roomData)
    else:
        room = Room(**roomData)
        rooms1d.append(room)

# For each group of rooms sharing a position pool, shuffle and assign
for position_key, group in flexible_groups.items():
    positions = [list(p) for p in eval(position_key)]  # recover positions from key
    random.shuffle(positions)
    for roomData, position in zip(group, positions):
        room = Room(**{**roomData, 'position': position})
        rooms1d.append(room)

# Now rooms1d is finalized, build the 2D grid
max_x = max(room.position[0] for room in rooms1d)
max_y = max(room.position[1] for room in rooms1d)

rooms2d: list[list[None | Room]] = [[None] * (max_y + 3) for _ in range(max_x + 3)]
for room in rooms1d:
    rooms2d[room.position[0] + 1][room.position[1] + 1] = room
