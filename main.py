# from player import Player
from room import Room
from directions import Direction
from coordinate import Coordinate


def main() -> None:
    print("Main")

    rooms: list[Room] = []

    # player: Player = Player(50.0)
    room: Room = Room(Coordinate(0, 0), "Entrance")
    rooms.append(room)
    print(rooms)


if __name__ == "__main__":
    main()
