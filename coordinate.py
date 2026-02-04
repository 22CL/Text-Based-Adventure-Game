from directions import Direction


class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        self.__coords: tuple[int, int] = (x, y)
    
    def move(self, direction: Direction):
        self.__coords = (self.__coords[0] + direction.value[0], self.__coords[1] + direction.value[1])
