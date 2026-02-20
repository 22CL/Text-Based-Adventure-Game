from .Entity import Entity
from src.items.items import Item


class BigSpider(Entity):
    def __init__(self, customId: str):
        super().__init__(customId, 30, 10, [Item("Cool Sword", 500, "goodsword")])
