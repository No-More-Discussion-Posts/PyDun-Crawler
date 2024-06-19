import pygame
import random
import sys
from pathlib import Path

from copd.engine.entities import *
from copd.ui.menus import PauseMenu, BattleMenu
from copd.config import DEFAULT_MAP
from copd.engine.states import GameStates
from copd.engine.ecs import Component
from copd.ui.tiles import TileMap
from copd.ui.map import Map
from copd.engine.input_handlers import EventHandler

# test
from copd.engine.systems import Movement, Collision, Turn, Combat
from copd.engine.components import Position, Velocity, TurnCounter
from copd.ui.minimap import MiniMap


# test
class Engine:

    def __init__(self):
        """Main Game Engine"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_CAPTION)
        self.components = {}
        self.debug = True
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
        self.treasures = pygame.sprite.LayeredUpdates()  # tagged for removal
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
        adds the player entitity
        to game, only called on game start

        """
        if player is None:
            self.player = Player("Bilbo", self, 15, 9, "player")
            self.player.draw()
        else:
            self.player = player
        self.Movement.add_entity(self.player)
        self.Collision.add_entity(self.player)
        self.Combat.add_entity(self.player)

    def load_map(self, map=DEFAULT_MAP) -> None:
        """
        Kills all sprite groups and loads a new map
        when the player collides with a door

        Parameters
        ----------
        color: Type: List, RGB value of wall color
        map: Type: Array, x and y coordinates of map tiles
        """
        # kills all non-player sprites
        self.monsters.empty()
        self.treasures.empty()
        self.doors.empty()
        self.solid_blocks.empty()
        # loads specififc map from args

        # add monster to game
        self.add_monster()

        self.current_room = Map(self, map)
        self.current_room.load_tiles()
        # add treasure for room
        self.add_treasure(14, 10)

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
        self.load_map()
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            if self.state == GameStates.BATTLE:
                BattleMenu(self).run()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def add_monster(self, monster=None):
        """
        Creates a random, or specific
        entity monster sprite
        """
        # allows selection of specific monsters(BOSSES)
        if monster is not None:
            self.monster = monster
        else:

            self.monster = create_monsters(self, randint(0, 2))
        self.Collision.add_entity(self.monster)
        self.Movement.add_entity(self.monster)

    def add_treasure(self, x, y):
        """
        creates a treasure sprite at coords
        ###TEST FUNCTION###

        Parameters
        ----------
        x : INT
        x tile position
        y : INT
        y tile position
        """
        self.treasure = Treasure(self, x, y)
