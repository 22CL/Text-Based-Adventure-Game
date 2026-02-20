import random
from typing import Final
import sys

from src.player import Player
from src.rooms import Room, get_rooms, get_room_at_player, get_next_room
from src.directions import Direction, DirectionError
from src.actions import Action, ActionError
from src.entities import BasicSpider, BigSpider
from src.items import Item


rooms: Final[list[list[None | Room]]] = get_rooms()

player: Player = Player(50.0, (1, 1))

running = True

canMoveToNextRoom = True

def main() -> None:
    global running

    print(f"You are in the: {get_room_at_player(player, rooms).name} room")

    while running:
        currentRoom: Room = get_room_at_player(player, rooms)
        if currentRoom.name == "Exit":
            print("Well done! You finished the game!")
            running = False
            break

        for item in currentRoom.items:
            print(f"You picked up: {item}")
            player.add_to_inventory(item)

        currentRoom.items = []

        if len(currentRoom.enemies) > 0:
            print(f"There are {len(currentRoom.enemies)} enemies")

        for enemyName in currentRoom.enemies:
            global enemy
            enemy = None
            selectedItemFromPlayer = Item("temporary item", -sys.maxsize, "temporaryitem")
            for item in player.get_inventory():
                if item.damageAmount > selectedItemFromPlayer.damageAmount:
                    selectedItemFromPlayer = item
            print(f"There is a {enemyName}!")
            if enemyName == "BasicSpider":
                enemy = BasicSpider(f"{currentRoom.name}BasicSpider")
            if enemyName == "BigSpider":
                enemy = BigSpider(f"{currentRoom.name}BigSpider")

            while enemy.get_health() > 0 and player.get_health() > 0:
                chance = random.randint(0, 10)
                if chance < 7:
                    print(f"You attack the spider dealing {selectedItemFromPlayer.damageAmount} damage!")
                    enemy.apply_damage(selectedItemFromPlayer.damageAmount)
                else:
                    print(f"The {enemyName} attacks you dealing {enemy.get_damage()} damage!")
                    player.apply_damage(enemy.get_damage())
            if player.get_health() > 0:
                print(f"You killed the {enemyName}!")
                print(f"You have {player.get_health()} health!")
            else:
                print(f"The {enemyName} killed you!")
                print("Try again to beat this game!")
                running = False
                break
        # Reset the enemies inside the room to stop repeated meeting of the enemies
        currentRoom.enemies = []
        # Check for player death so you cannot try to move after death
        if not running:
            break

        print(f"\n{player}")

        userAction: Action | ActionError = Action.from_input(str(input(">> ")).upper())
        if type(userAction) == ActionError:
            print(userAction.response)
        else:
            surrounding_rooms: dict[Direction, None | Room] = {
                Direction.NORTH: get_next_room(player, Direction.NORTH, rooms),
                Direction.EAST: get_next_room(player, Direction.EAST, rooms),
                Direction.SOUTH: get_next_room(player, Direction.SOUTH, rooms),
                Direction.WEST: get_next_room(player, Direction.WEST, rooms),
            }

            match userAction:
                case Action.MOVE:
                    direction: Direction | DirectionError = Direction.from_input(str(input("Which direction? ")))
                    if type(direction) == DirectionError:
                        print(direction.response)

                    global canMoveToNextRoom  # For the loops below
                    canMoveToNextRoom = True

                    response: str = ""

                    nextRoom: Room | None = surrounding_rooms[direction]

                    if nextRoom is None:
                        canMoveToNextRoom = False
                        response = "That is a wall!"
                    else:
                        if nextRoom.locked:
                            inventory = player.get_inventory()
                            for item in inventory:
                                if item.itemId == nextRoom.requiredItemToOpenId:
                                    response = "You unlocked that door!"
                                    nextRoom.locked = False
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

                    print(f"You are in the: {get_room_at_player(player, rooms).name} room")
                case Action.LOOK:
                    print(f"You are in the {get_room_at_player(player, rooms).name}!")
                    if surrounding_rooms[Direction.NORTH] is not None:
                        print(f"North is: {surrounding_rooms[Direction.NORTH].name}")
                    else:
                        print(f"North is a wall!")
                    if surrounding_rooms[Direction.EAST] is not None:
                        print(f"East is: {surrounding_rooms[Direction.EAST].name}")
                    else:
                        print(f"East is a wall!")
                    if surrounding_rooms[Direction.SOUTH] is not None:
                        print(f"South is: {surrounding_rooms[Direction.SOUTH].name}")
                    else:
                        print(f"South is a wall!")
                    if surrounding_rooms[Direction.WEST] is not None:
                        print(f"West is: {surrounding_rooms[Direction.WEST].name}")
                    else:
                        print(f"West is a wall!")
                case Action.EXIT:
                    print("Goodbye")
                    running = False
                case Action.GET_INVENTORY:
                    print(player.get_inventory())
                case _:
                    print("Sorry, Action checks failed! This is a bug! Try again!")


if __name__ == "__main__":
    main()
