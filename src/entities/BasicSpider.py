from .Entity import Entity
from ..items.items import Sword


class BasicSpider(Entity):
    def __init__(self):
        super().__init__(5, 1, [Sword("Weak Sword", 5)])
