from .directions import Direction
from .items.items import Item, Sword


class Player:
    def __init__(self, health: float, coord: tuple[int, int]) -> None:
        self.__health: float = health
        self.__coord: tuple[int, int] = coord
        self.__inventory: list[Item] = []

        self.__inventory.append(Sword("Weak Sword", 50000))
    
    def __repr__(self) -> str:
        return (f"Player Stats:\n"
                f"Health: {self.__health}\n"
                f"Position: {self.__coord}\n"
                )
    
    def get_health(self) -> float:
        return self.__health

    def apply_damage(self, damage: float):
        self.__health -= damage
    
    def move(self, direction: Direction):
        self.__coord = (self.__coord[0] + direction.value[0], self.__coord[1] + direction.value[1])

    def get_coordinates(self) -> tuple[int, int]:
        return self.__coord[0], self.__coord[1]
