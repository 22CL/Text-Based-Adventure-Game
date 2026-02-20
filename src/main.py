import asyncio
import random
from typing import Final
from textual.app import ComposeResult, App
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Footer, Header, Button, Static, Digits
from textual.binding import Binding
from textual import work

from src.player import Player
from src.rooms import Room, get_rooms, get_room_at_player, get_next_room
from src.directions import Direction, DirectionError
from src.entities import BasicSpider, BigSpider
from src.items import Item


class TextBasedAdventureGame(App):
    def __init__(self):
        super().__init__()

        self.player: Player = Player(50, (1, 1))
        self.rooms: Final[list[list[None | Room]]] = get_rooms()
        self.canMoveToNextRoom: bool = False
        self.currentRoom: Room = get_room_at_player(self.player, self.rooms)
        self.direction: Direction = None
        self.in_combat: bool = False

        self.currentAction: str = "Hello"
        self.game_over: bool = False

        self.currentAction = f"You are in the: {get_room_at_player(self.player, self.rooms).name} room"

    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding(key='q', action='quit', description='Quit the game'),
        Binding(key='tab', action='tab', description='Tab down'),
        Binding(key='ctrl+tab', action='reverse_tab', description='Tab back up'),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Digits(str(self.player.get_health()), classes='player_health_tracker')
        yield Horizontal(
            VerticalScroll(
                Static("Actions", classes='header'),
                Button("Move", id="move_btn"),
                Button("Look"),
                Button("Get Inventory"),
                Button("Damage"),
            ),
            Vertical(
                Button("North", id="North", classes="direction_btn"),
                Button("South", id="South", classes="direction_btn"),
                Button("East",  id="East",  classes="direction_btn"),
                Button("West",  id="West",  classes="direction_btn"),
                id="move_menu",
            ),
            Static("You entered the game!", classes='current_action'),
        )

    def do_look(self) -> None:
        surrounding_rooms = {
            Direction.NORTH: get_next_room(self.player, Direction.NORTH, self.rooms),
            Direction.EAST:  get_next_room(self.player, Direction.EAST,  self.rooms),
            Direction.SOUTH: get_next_room(self.player, Direction.SOUTH, self.rooms),
            Direction.WEST:  get_next_room(self.player, Direction.WEST,  self.rooms),
        }
        lines = [f"You are in the {self.currentRoom.name}!"]
        for d, room in surrounding_rooms.items():
            lines.append(f"{d.name.capitalize()} is: {room.name if room else 'a wall!'}")
        self.currentAction = "\n".join(lines)
        self.visual_update()

    def do_move(self, direction_str: str) -> None:
        direction = Direction.from_input(direction_str.upper())
        surrounding_rooms = {
            Direction.NORTH: get_next_room(self.player, Direction.NORTH, self.rooms),
            Direction.EAST:  get_next_room(self.player, Direction.EAST,  self.rooms),
            Direction.SOUTH: get_next_room(self.player, Direction.SOUTH, self.rooms),
            Direction.WEST:  get_next_room(self.player, Direction.WEST,  self.rooms),
        }

        if type(direction) is DirectionError:
            self.currentAction = direction.response
            self.visual_update()
            return

        nextRoom = surrounding_rooms[direction]
        if nextRoom is None:
            self.currentAction = "That is a wall!"
            self.visual_update()
        elif nextRoom.locked:
            for item in self.player.get_inventory():
                if item.itemId == nextRoom.requiredItemToOpenId:
                    nextRoom.locked = False
                    self.player.move(direction)
                    self.currentAction = "You unlocked that door!"
                    self.visual_update()
                    self.enter_room()
                    break
            else:
                self.currentAction = "Sorry, that room is locked!"
                self.visual_update()
        else:
            self.player.move(direction)
            self.enter_room()

    def do_get_inventory(self) -> None:
        inventory = self.player.get_inventory()
        if inventory:
            self.currentAction = "You have:\n" + "\n".join(item.name for item in inventory)
        else:
            self.currentAction = "Your inventory is empty!"
        self.visual_update()

    @work
    async def enter_room(self) -> None:
        self.currentRoom = get_room_at_player(self.player, self.rooms)
        self.sub_title = self.currentRoom.name

        if self.currentRoom.name == "Exit":
            self.currentAction = "Well done! You finished the game!"
            self.visual_update()
            self.set_timer(3, self.exit())
            return

        # Item pickup
        for itemList in self.currentRoom.items:
            item = Item(name=itemList[0], damageAmount=itemList[1], itemId=itemList[2])
            self.currentAction = f"You picked up: {item.name}"
            self.player.add_to_inventory(item)
            self.visual_update()
            await asyncio.sleep(1)
        self.currentRoom.items = []

        # Enemy logic
        self.in_combat = True
        for enemyName in self.currentRoom.enemies:
            selectedItem = Item("Fists", 1, "fists")
            for item in self.player.get_inventory():
                if item.damageAmount > selectedItem.damageAmount:
                    selectedItem = item

            self.currentAction = f"There is a {enemyName}!"
            self.visual_update()
            await asyncio.sleep(1)

            enemy = None
            if enemyName == "BasicSpider":
                enemy = BasicSpider(f"{self.currentRoom.name}BasicSpider")
            if enemyName == "BigSpider":
                enemy = BigSpider(f"{self.currentRoom.name}BigSpider")

            while enemy.get_health() > 0 and self.player.get_health() > 0:
                chance = random.randint(0, 10)
                if chance < 7:
                    self.currentAction = f"You attack the {enemyName} dealing {selectedItem.damageAmount} damage!"
                    enemy.apply_damage(selectedItem.damageAmount)
                else:
                    self.currentAction = f"The {enemyName} attacks you dealing {enemy.get_damage()} damage!"
                    self.player.apply_damage(enemy.get_damage())
                self.visual_update()
                await asyncio.sleep(1)

                if self.player.get_health() <= 0:
                    return  # visual_update already handles death display

            self.currentAction = f"You killed the {enemyName}!"
            self.visual_update()
            await asyncio.sleep(0.5)

            for lootItem in enemy.get_loot():
                self.player.add_to_inventory(lootItem)
                self.currentAction = f"You looted: {lootItem.name}"
                self.visual_update()
                await asyncio.sleep(0.5)

        self.currentRoom.enemies = []
        self.in_combat = False
        self.currentAction = f"You are in the: {self.currentRoom.name} room"
        self.visual_update()

    def visual_update(self) -> None:
        self.query_one('.player_health_tracker').update(str(self.player.get_health()))
        if self.player.get_health() <= 0:
            self.game_over = True
            self.query_one('.current_action').update("YOU DIED! GAME OVER!")
            self.set_timer(3, self.exit)
        else:
            self.query_one('.current_action').update(str(self.currentAction))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if self.game_over or self.in_combat:
            return

        if event.button.id == "move_btn":
            menu = self.query_one("#move_menu")
            menu.display = not menu.display
            if menu.display:
                self.set_focus(menu.query_one(Button))
            return

        if "direction_btn" in event.button.classes:
            direction = event.button.id
            self.query_one("#move_menu").display = False
            self.set_focus(self.query_one("#move_btn"))
            self.do_move(direction)
            return

        match event.button.label:
            case "Look":
                self.do_look()
            case "Get Inventory":
                self.do_get_inventory()
            case "Damage":
                self.player.apply_damage(5)
                self.visual_update()

    def on_key(self, event) -> None:
        if self.game_over or self.in_combat:
            event.prevent_default()
            return

        menu = self.query_one("#move_menu")
        sidebar = self.query_one(VerticalScroll)

        if menu.display:
            buttons = menu.query(Button)
            if event.key == "escape":
                menu.display = False
                self.set_focus(self.query_one("#move_btn"))
                return
            if event.key == "tab" and self.focused == buttons.last():
                event.prevent_default()
                self.set_focus(buttons.first())
            if event.key == "ctrl+tab" and self.focused == buttons.first():
                event.prevent_default()
                self.set_focus(buttons.last())
            return

        sidebar_buttons = sidebar.query(Button)
        if event.key == "tab" and self.focused == sidebar_buttons.last():
            event.prevent_default()
            self.set_focus(sidebar_buttons.first())
        if event.key == "ctrl+tab" and self.focused == sidebar_buttons.first():
            event.prevent_default()
            self.set_focus(sidebar_buttons.last())

    def action_reverse_tab(self) -> None:
        pass  # handled in on_key

    def action_tab(self) -> None:
        pass  # handled in on_key

    def on_mount(self) -> None:
        self.title = "Text Based Adventure Game"
        self.sub_title = get_room_at_player(self.player, self.rooms).name


if __name__ == "__main__":
    app = TextBasedAdventureGame()
    app.run()
