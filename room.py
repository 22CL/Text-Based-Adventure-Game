from typing import Final
from coordinate import Coordinate


class Room:
    def __init__(self, coords: Coordinate, name: str):
        self.__coords: Final[Coordinate] = coords
        self.__name: str = name
    
    def __repr__(self) -> str:
        return f"{self.__name}: {self.__coords}"
    