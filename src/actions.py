from enum import Enum
from typing import Final


class Action(Enum):
    MOVE = "move"
    EXIT = "exit"
    LOOK = "look"
    ERROR = "error"
    GET_INVENTORY = "i"

    @classmethod
    def from_input(cls, userInput: str) -> Action | ActionError:
        if cls.__contains__(userInput.lower()):
            return cls(userInput.lower())
        return ActionError()

class ActionError(Exception):
    value: Final[Action.ERROR] = Action.ERROR
    response: str = "Sorry, that is not a valid action!"
    pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"
