import enum
from coordinate import Coordinate
from typing import Any


class Direction(enum.Enum):
    NORTH = 1, 0
    SOUTH = -1, 0
    EAST = 0, 1
    WEST = 0, -1

    def add(self, coord: Coordinate, direction: Any) -> tuple[int, int]:
        return (coord[0] + direction.value[0], coord[1] + direction.value[1])