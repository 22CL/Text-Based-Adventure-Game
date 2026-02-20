class Item:
    def __init__(self, name: str, damageAmount: int, itemId: str) -> None:
        self.name = name
        self.damageAmount = damageAmount
        self.itemId = itemId

    def __repr__(self) -> str:
        return f"name: {self.name} id: {self.itemId}, damage: {self.damageAmount}"
