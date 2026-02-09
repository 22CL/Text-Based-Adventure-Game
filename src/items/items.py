class Item:
    def __init__(self, name: str, damageAmount: int) -> None:
        self.name = name
        self.damageAmount = damageAmount

class Sword(Item):
    def __init__(self, name: str, damageAmount: int) -> None:
        super().__init__(name, damageAmount)

class Key(Item):
    def __init__(self, name: str) -> None:
        super().__init__(name, 0)
