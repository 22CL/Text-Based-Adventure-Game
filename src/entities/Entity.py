from src.items.items import Item


class Entity:
    def __init__(self, customId: str, health: int, damage: int, loot: list[Item]):
        self.__health: int = health
        self.__damage: int = damage
        self.__loot: list[Item] = loot
        self.__dead: bool = False
        self.__id: str = customId

    def get_health(self) -> int:
        return self.__health

    def apply_damage(self, damage: int) -> None:
        self.__health -= damage

    def get_damage(self) -> int:
        return self.__damage

    def get_loot(self) -> list[Item]:
        loot: list[Item] = self.__loot
        self.__loot = []
        return loot
