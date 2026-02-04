from coordinate import Coordinate
from directions import Direction


class Player:
    def __init__(self, health: float, coord: Coordinate) -> None:
        self.__health: float = health
        self.__coord: Coordinate = coord
    
    def __repr__(self) -> str:
        return f"Health: {self.__health}"
    
    def get_health(self) -> float:
        return self.__health

    def apply_damage(self, damage: float):
        self.__health -= damage
    
    def move(self, direction: Direction):
        self.__coord = 