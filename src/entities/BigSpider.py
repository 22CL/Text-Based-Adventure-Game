from .Entity import Entity
from ..items.items import Sword


class BigSpider(Entity):
    def __init__(self):
        super().__init__(30, 10, [Sword("Cool Sword", 500)])
