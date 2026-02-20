from src.directions import Direction
from src.items.items import Item


class Player:
    def __init__(self, health: float, position: tuple[int, int]) -> None:
        self.health: float = health
        self.position: tuple[int, int] = position
        self.inventory: list[Item] = []

        self.inventory.append(Item("Weak Sword", 5, "weaksword"))
    
    def __repr__(self) -> str:
        return (f"Player Stats:\n"
                f"Health: {self.health}\n"
                f"Position: {self.position}\n"
                )

    def has_item(self, item_type) -> bool:
        return any(isinstance(item, item_type) for item in self.inventory)

    def get_item(self, item_type) -> Item:
        return next(
            (item for item in self.inventory if isinstance(item, item_type)),
            None
        )

    def get_health(self) -> float:
        return self.health

    def apply_damage(self, damage: float):
        self.health -= damage
    
    def move(self, direction: Direction):
        self.position = (self.position[0] + direction.value[0], self.position[1] + direction.value[1])

    def get_position(self) -> tuple[int, int]:
        return self.position[0], self.position[1]

    def get_inventory(self) -> list[Item]:
        return self.inventory

    def add_to_inventory(self, item: Item):
        self.inventory.append(item)

    def remove_from_inventory(self, item: Item):
        self.inventory.remove(item)
