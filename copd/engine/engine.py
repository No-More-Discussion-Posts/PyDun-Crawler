import pygame
import random
from random import randrange
import sys
from pathlib import Path

from copd.engine.entities import *
from copd.ui.menus import PauseMenu, BattleMenu, MainMenu, GameOver
from copd.config import DEFAULT_MAP
from copd.engine.states import GameStates
from copd.engine.ecs import Component
from copd.ui.tiles import TileMap
from copd.ui.map import Map
from copd.engine.input_handlers import EventHandler
from copd.engine.systems import Movement, Collision, Turn, Combat
from copd.engine.components import Position, Velocity, TurnCounter
from copd.ui.minimap import MiniMap


class Engine:

    def __init__(self):
        """Main Game Engine"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_CAPTION)
        self.components = {}
        self.debug = False
        self.Turn = Turn()
        self.running = False
        # will need to change state when changing between menus
        self.state = GameStates.MAIN
        self.enemies = []
        self.event_handler = EventHandler(self)
        self.handle_event = self.event_handler.handle_event
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.solid_blocks = pygame.sprite.LayeredUpdates()
        self.monsters = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.treasures = pygame.sprite.LayeredUpdates()
        self.Movement = Movement()
        self.Collision = Collision()
        self.Combat = Combat(self)
        self.Turn.add_entity(self)
        self.add_component(TurnCounter())
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.minimap = MiniMap(self)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_CAPTION)
        self.tile_map = TileMap(Path("copd/ui/assets/tilemap.png"))
        self.room_states = {}
        self.enemies_killed = 0
        self.rooms = {} 
        # {"room_id": None ,
                    #   "mapname": None}}

    def add_component(self, component: Component):
        """_summary_

        Parameters
        ----------
        component : Component
            Component to be added to the Engine
        """
        self.components[type(component)] = component

    def get(self, component):
        return self.components.get(component)

    def add_player(self, player=None) -> None:
        """
        adds the player entity
        to game, only called on game start
        """
        if player is None:
            self.player = Player("Bilbo", self, 15, 9, "player")
            self.player.draw()
        else:
            self.player = player

    def load_map(self) -> None:
        """
        Kills all sprite groups and loads a new map
        when the player collides with a door

        Parameters
        ----------
        color: Type: List, RGB value of wall color
        map: Type: Array, x and y coordinates of map tiles
        """
        if self.rooms.get(self.get_room_id()) == None:
            mapchoice = randrange(3)
            match mapchoice:
                case 0:
                    map = DEFAULT_MAP
                    self.rooms[self.get_room_id()] = DEFAULT_MAP
                case 1:
                    map = MAZE
                    self.rooms[self.get_room_id()] = MAZE
                case 2:
                    map = MAP1
                    self.rooms[self.get_room_id()] = MAP1
                case 3:
                    map = MAP2
                    self.rooms[self.get_room_id()] = MAP2
        map = self.rooms[self.get_room_id()]
        #else:
            #map = DEFAULT_MAP
            #self.room_type[self.get_room_id]["mapname"] = DEFAULT_MAP
        # kills all non-player sprites
        self.monsters.empty()
        self.treasures.empty()
        self.doors.empty()
        self.solid_blocks.empty()

        # Get the unique identifier for the current room
        room_id = self.get_room_id()

        # Retrieve the room state if it exists, otherwise initialize it
        room_state = self.room_states.get(room_id, {"treasures": [], "enemies": [], "roomtype": []})





        # Load treasures from the room state
        for treasure_info in room_state["treasures"]:
            x, y, collected = treasure_info
            if not collected:
                treasure = Treasure(self, x, y, collected=collected)
                self.treasures.add(treasure)
                treasure.draw()

        # Load enemies from the room state
        for enemy_info in room_state["enemies"]:
            enemy_type, x, y, alive = enemy_info
            if alive:
                enemy = create_monster(self, x, y, number=enemy_type)
                self.monsters.add(enemy)
                self.Collision.add_entity(enemy)
                self.Movement.add_entity(enemy)
                enemy.draw()
        
        self.current_room = Map(self, map)
        self.current_room.load_tiles()

        # Add new monsters and treasures if they do not already exist in the room state
        if not room_state["enemies"]:
            self.add_monster()

        if not room_state["treasures"]:
            self.add_treasure()

    def get_room_id(self):
        """Returns a unique identifier for the current room."""
        return tuple(self.player.overworldcoords)

    def update(self):
        """Update all sprites"""
        self.all_sprites.update()
        self.players.update()
        self.monster.update()

    def draw(self):
        """
        Draws all sprites, minimap,
        and turn counter to screen
        """
        self.screen.fill(Colors.BLACK)
        self.all_sprites.draw(self.screen)
        self.blocks.draw(self.screen)
        self.solid_blocks.draw(self.screen)
        self.monsters.draw(self.screen)
        self.players.draw(self.screen)
        self.doors.draw(self.screen)
        self.treasures.draw(self.screen)
        self.show_turn()
        self.minimap.draw()
        self.clock.tick(FPS)
        pygame.display.update()

    def show_turn(self):
        # displays turn counter
        font = pygame.font.get_default_font()
        FONT = pygame.font.Font(font, TILE_SIZE)
        turn = FONT.render(str(self.get(TurnCounter).turn), False, "yellow")
        self.screen.blit(turn, (TILE_SIZE, 0))

    def run(self):
        self.running = True
        MainMenu(self).run()

        self.add_player()
        self.load_map()
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            if self.state == GameStates.BATTLE:
                BattleMenu(self).run()
            self.update()
            self.draw()
            if self.enemies_killed >= 5:
                break
        GameOver(self).run()
        pygame.quit()
        sys.exit()

    def add_monster(self, monster=None):
        """
        Creates a random, or specific
        entity monster sprite
        """
        room_id = self.get_room_id()
        room_state = self.room_states.get(room_id, {"treasures": [], "enemies": []})

        if monster is not None:
            self.monster = monster
        else:
            valid_positions = self.current_room.valid_positions
            if not valid_positions:
                print("No valid positions available to spawn monsters.")
                return

            x, y = random.choice(valid_positions)
            self.monster = create_monster(self, x, y)

        if self.monster is None:
            print("Failed to create a monster.")
            return

        self.Collision.add_entity(self.monster)
        self.Movement.add_entity(self.monster)

        # Add the monster to the room state if it doesn't already exist
        if not any(
            enemy
            for enemy in room_state["enemies"]
            if enemy[1] == self.monster.rect.x // TILE_SIZE
            and enemy[2] == self.monster.rect.y // TILE_SIZE
        ):
            room_state["enemies"].append(
                (
                    self.monster.type,
                    self.monster.rect.x // TILE_SIZE,
                    self.monster.rect.y // TILE_SIZE,
                    True,
                )
            )
            self.room_states[room_id] = room_state

        self.monsters.add(self.monster)
        self.monster.draw()

    def add_treasure(self):
        """
        Creates a treasure sprite at coords
        ###TEST FUNCTION###

        Parameters
        ----------
        x : INT
        x tile position
        y : INT
        y tile position
        """
        room_id = self.get_room_id()
        room_state = self.room_states.get(room_id, {"treasures": [], "enemies": []})

        valid_positions = self.current_room.valid_positions
        x, y = random.choice(valid_positions)
        self.treasure = Treasure(self, x, y)

        # Add the treasure to the room state if it doesn't already exist
        if not any(
            treasure
            for treasure in room_state["treasures"]
            if treasure[0] == x and treasure[1] == y
        ):
            room_state["treasures"].append((x, y, False))
            self.room_states[room_id] = room_state

        self.treasures.add(self.treasure)
        self.treasure.draw()

    def update_room_state(self):
        """
        Updates the room state based on the current state of treasures and monsters
        """
        room_id = self.get_room_id()
        room_state = self.room_states.get(room_id, {"treasures": [], "enemies": []})

        # Update treasures
        for treasure in self.treasures:
            for idx, (x, y, collected) in enumerate(room_state["treasures"]):
                if (
                    treasure.rect.x // TILE_SIZE == x
                    and treasure.rect.y // TILE_SIZE == y
                ):
                    room_state["treasures"][idx] = (x, y, True)

        # Update enemies
        for monster in self.monsters:
            for idx, (enemy_type, x, y, alive) in enumerate(room_state["enemies"]):
                if (
                    monster.rect.x // TILE_SIZE == x
                    and monster.rect.y // TILE_SIZE == y
                ):
                    room_state["enemies"][idx] = (enemy_type, x, y, False)

        self.room_states[room_id] = room_state
