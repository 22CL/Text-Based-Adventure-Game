from src.directions import Direction
from src.items.items import Item, Sword


class Player:
    def __init__(self, health: float, coord: tuple[int, int]) -> None:
        self.__health: float = health
        self.__coord: tuple[int, int] = coord
        self.__inventory: list[Item] = []

        self.__inventory.append(Sword("Weak Sword", 5, "weaksword"))
    
    def __repr__(self) -> str:
        return (f"Player Stats:\n"
                f"Health: {self.__health}\n"
                f"Position: {self.__coord}\n"
                )

    def has(self, item_type) -> bool:
        return any(isinstance(item, item_type) for item in self.__inventory)

    def get(self, item_type) -> Item:
        return next(
            (item for item in self.__inventory if isinstance(item, item_type)),
            None
        )

    def get_health(self) -> float:
        return self.__health

    def apply_damage(self, damage: float):
        self.__health -= damage
    
    def move(self, direction: Direction):
        self.__coord = (self.__coord[0] + direction.value[0], self.__coord[1] + direction.value[1])

    def get_coordinates(self) -> tuple[int, int]:
        return self.__coord[0], self.__coord[1]

    def get_inventory(self) -> list[Item]:
        return self.__inventory

    def add_to_inventory(self, item: Item):
        self.__inventory.append(item)

    def remove_from_inventory(self, item: Item):
        self.__inventory.remove(item)
