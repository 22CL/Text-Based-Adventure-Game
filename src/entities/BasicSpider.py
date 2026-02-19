from .Entity import Entity
from src.items.items import Sword


class BasicSpider(Entity):
    def __init__(self, customId: str) -> None:
        super().__init__(customId, 5, 1, [Sword("Weak Sword", 5, "weaksword")])
