from src.player import Player
from src.rooms import Room, setup_rooms
from src.directions import Direction, DirectionError
from src.actions import Action, ActionError
from src.items.items import Sword, Item, Key
from copy import deepcopy


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
        if currentRoom.get_name() == "Exit":
            print("Well done! You finished the game!")
            running = False
            break

        for item in currentRoom.items:
            print(f"You picked up: {item}")
            player.add_to_inventory(item)

        currentRoom.items = []

        enemies = deepcopy(currentRoom.enemies)
        if len(enemies) != 0:
            print("Enemy is alive!")
            for enemy in currentRoom.enemies:
                print(f"Enemy: {enemy.__class__.__name__} with {enemy.get_health()} health")
                while enemy.get_health() > -1 and player.get_health() > 0:
                    if enemy.get_health() > 0:
                        playerWeapon: Item = Sword("TEMP", -100000000, "tempsword")
                        for item in player.get_inventory():
                            if item.damageAmount > playerWeapon.damageAmount:
                                playerWeapon = item
                        enemy.apply_damage(playerWeapon.damageAmount)
                        print(f"Applied {playerWeapon.damageAmount} damage!")

                        print(f"Enemy attacked with {enemy.get_damage()} damage!")
                        player.apply_damage(enemy.get_damage())
                        print(f"Player health at {player.get_health()} health!")
                    else:
                        enemy.get_loot()
                        currentRoom.enemies.remove(enemy)
                        print("Enemy killed!")
                        break

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

                    global canMoveToNextRoom  # For the loops below
                    canMoveToNextRoom = True

                    response: str = ""

                    nextRoom: Room = rooms[
                        player.get_coordinates()[0] + direction.value[0]][player.get_coordinates()[1] + direction.value[1]]

                    if nextRoom is None:
                        canMoveToNextRoom = False
                        response = "That is a wall!"
                        print("FAILED None check!")
                    else:
                        if nextRoom.get_locked_state():
                            playerInventory = player.get_inventory()
                            for item in playerInventory:
                                if isinstance(item, Key) and item.name == "Locked door key" and item.itemId == "lockeddoorkey":
                                    response = "You unlocked that door!"
                                    nextRoom.unlock()
                                    canMoveToNextRoom = True
                                    break
                            else:
                                # ONLY IF break IS NOT CALLED!
                                response = "Sorry, that room is locked!"
                                canMoveToNextRoom = False

                    if response != "":
                        print(response)

                    if canMoveToNextRoom:
                        player.move(direction)

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
                case Action.GET_INVENTORY:
                    print(player.get_inventory())
                case _:
                    print("Sorry, Action checks failed! This is a bug! Try again!")


if __name__ == "__main__":
    main()
