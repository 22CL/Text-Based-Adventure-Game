class Item:
    def __init__(self, name: str, damageAmount: int, itemId: str) -> None:
        self.name = name
        self.damageAmount = damageAmount
        self.itemId = itemId

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} -> {self.name}: id: {self.itemId}, damage: {self.damageAmount}"

class Sword(Item):
    def __init__(self, name: str, damageAmount: int, itemId: str) -> None:
        super().__init__(name, damageAmount, itemId)

class Key(Item):
    def __init__(self, name: str, itemId: str) -> None:
        super().__init__(name, 0, itemId)
