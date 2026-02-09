from enum import Enum


class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    @classmethod
    def from_input(cls, userInput: str) -> Direction | DirectionError:
        if userInput.upper() in cls.__members__:
            return cls[userInput.upper()]
        return DirectionError()

class DirectionError(Exception):
    value: tuple[int, int] = (0, 0)
    response: str = "Sorry, that is not a valid direction!"
    pass
