from .Entity import Entity
from src.items.items import Item


class BasicSpider(Entity):
    def __init__(self, customId: str) -> None:
        super().__init__(customId, 10, 1, [Item("Weak Sword", 5, "weaksword")])
