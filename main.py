from src.player import Player
from src.rooms import Room, setup_rooms
from src.directions import Direction, DirectionError
from src.actions import Action, ActionError


# Rows = y, Cols = x DON'T FORGET THAT!
rows, cols = 7, 7
rooms: list[list[None | Room]] = [[None] * rows for _ in range(cols)]

player: Player = Player(50.0, (1, 3))

running = True

def get_room_at_player() -> Room:
    return rooms[player.get_coordinates()[0]][player.get_coordinates()[1]]


def main() -> None:
    global running
    print(player)

    setup_rooms(rooms)
    print(get_room_at_player())

    while running:
        currentRoom: Room = get_room_at_player()
        if len(currentRoom.enemies) != 0:
            print("Enemy is alive!")

        userAction: Action | ActionError = Action.from_input(str(input(">> ")).upper())

        if type(userAction) == ActionError:
            print(userAction.response)
        else:
            surrounding_rooms = {
                Direction.NORTH: rooms[player.get_coordinates()[0] + Direction.NORTH.value[0]][player.get_coordinates()[1] + Direction.NORTH.value[1]],
                Direction.SOUTH: rooms[player.get_coordinates()[0] + Direction.SOUTH.value[0]][player.get_coordinates()[1] + Direction.SOUTH.value[1]],
                Direction.EAST: rooms[player.get_coordinates()[0] + Direction.EAST.value[0]][player.get_coordinates()[1] + Direction.EAST.value[1]],
                Direction.WEST: rooms[player.get_coordinates()[0] + Direction.WEST.value[0]][player.get_coordinates()[1] + Direction.WEST.value[1]],
            }

            match userAction:
                case Action.MOVE:
                    direction: Direction | DirectionError = Direction.from_input(str(input("Which direction? ")))
                    if type(direction) == DirectionError:
                        print(direction.response)

                    nextRoom: Room = rooms[
                        player.get_coordinates()[0] + direction.value[0]][player.get_coordinates()[1] + direction.value[1]]
                    if nextRoom is not None:
                        player.move(direction)
                    else:
                        print("Sorry, that's a wall!")
                    print(get_room_at_player())
                case Action.LOOK:
                    print(f"You are in the {get_room_at_player()}!")
                    print(f"North is: {surrounding_rooms[Direction.NORTH]}")
                    print(f"East is: {surrounding_rooms[Direction.EAST]}")
                    print(f"South is: {surrounding_rooms[Direction.SOUTH]}")
                    print(f"West is: {surrounding_rooms[Direction.WEST]}")
                case Action.EXIT:
                    print("Goodbye")
                    running = False
                case _:
                    print("Sorry, Action checks failed! This is a bug!")


if __name__ == "__main__":
    main()
