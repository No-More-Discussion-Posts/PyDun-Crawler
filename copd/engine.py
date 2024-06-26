import pygame
import random
import sys

from .entities import *
from .menus import PauseMenu, BattleMenu
from .config import DEFAULT_MAP
from .ecs.states import GameStates
from .ecs.ecs import Component
from .input_handlers import EventHandler

# test
from .ecs.systems import Movement, Collision, Turn
from .ecs.components import Position, Velocity, TurnCounter


# test
class Engine:

    def __init__(self):
        """Main Game Engine"""
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
        self.monsters = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.treasures = pygame.sprite.LayeredUpdates()
        self.Movement = Movement()
        self.Collision = Collision()
        self.Turn.add_entity(self)
        self.add_component(TurnCounter())

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
            self.player = Player("Bilbo", self, 15, 9)
            self.player.add_component(Position(15, 9))
            self.player.add_component(Velocity())
        else:
            self.player = player
        self.Movement.add_entity(self.player)
        self.Collision.add_entity(self.player)

    def load_start_map(self, color, map=None) -> None:
        """
        loads starting map
        Parameters
        ----------
        color: Type: List, RGB value of wall color
        map: Type: Array, x and y coordinates of map tiles
        """
        if map is not None:
            # accepts alternate map
            map = map
        else:
            # load default starting map
            map = DEFAULT_MAP

        # add player to game
        self.add_player()
        # add monster sprite to game
        self.add_monster()
        # add wall sprites around perimiter of map
        self.create_walls(map, color)
        # add treasure sprite to game
        self.add_treasure(14, 10)

    def load_map(self, color, map=None) -> None:
        """
        Kills all sprite groups and loads a new map
        when the player collides with a door

        Parameters
        ----------
        color: Type: List, RGB value of wall color
        map: Type: Array, x and y coordinates of map tiles
        """
        # loads specififc map from args
        if map is not None:
            map = map
        # loads default map
        else:
            map = DEFAULT_MAP
        # kills all non-player sprites
        pygame.sprite.Group.empty(self.blocks)
        self.monster.kill()
        # add monster to game
        self.add_monster()
        # add walls to border
        self.create_walls(map, color)
        # add treasure for room
        self.add_treasure(14, 10)

    def draw(self):
        """
        Draws all sprites, minimap,
        and turn counter to screen
        """
        self.all_sprites.draw(self.screen)
        self.players.draw(self.screen)
        self.blocks.draw(self.screen)
        self.monsters.draw(self.screen)
        self.doors.draw(self.screen)
        self.treasures.draw(self.screen)
        self.show_turn()
        self.show_location()

        pygame.display.update()

    def show_turn(self):
        # displays turn counter
        font = pygame.font.get_default_font()
        FONT = pygame.font.Font(font, TILE_SIZE)
        turn = FONT.render(str(self.get(TurnCounter).turn), False, "black")
        self.screen.blit(turn, (20, 20))
        # self.screen.blit(turn,(TILE_SIZE*2,SCREEN_WIDTH-(TILE_SIZE*2)))

    def show_location(self):
        # displays turn counter
        font = pygame.font.get_default_font()
        FONT = pygame.font.Font(font, TILE_SIZE)
        coords = FONT.render(str(self.player.overworldcoords), False, "black")
        self.screen.blit(coords, (29 * TILE_SIZE, 20))
        # self.screen.blit(turn,(TILE_SIZE*2,SCREEN_WIDTH-(TILE_SIZE*2)))

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_CAPTION)
        self.draw()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            if self.state == GameStates.BATTLE:
                BattleMenu(self).run()
            self.draw()
        pygame.quit()
        sys.exit()

    def Test_Grid(self):
        """
        draws 20 x 20 squares across game screen
        """
        for x in range(0, 640, 20):
            pygame.draw.line(self.screen, (128, 128, 128), (x, 0), (x, 360))
        # draw lines vertically
        for y in range(0, 360, 20):
            pygame.draw.line(self.screen, (128, 128, 128), (0, y), (640, y))

    def add_monster(self, monster=None):
        """
        Creates a random, or specific
        entity monster sprite
        """
        # allows selection of specific monsters(BOSSES)
        if monster is not None:
            self.monster = monster
        else:
            # if no monster is supplied
            # initilizes random enemy sprite in room
            num = random.randint(1, 3)
            if num == 1:
                self.monster = Goblin(self)
            if num == 2:
                self.monster = HobGoblin(self)
            if num == 3:
                self.monster = Ogre(self)

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

    def door_or_walls(self):
        """
        overworld_map:
        [0, 0], [1, 0], [2, 0]
        [0, 1], [1, 1], [2, 1]
        [0, 2], [1, 2], [2, 2]
        """

        # up and down
        if self.player.overworldcoords[1] == 0:  # if north border
            Wall(self, 17, 0, BLUE)  # draw wall at north door
        else:
            Door(self, 17, 0)  # draw north door
        if self.player.overworldcoords[1] == 2:  # if south border
            Wall(self, 17, 17, BLUE)  # draw wall at south door
        else:
            Door(self, 17, 17)  # draw south door

        # left and right
        if self.player.overworldcoords[0] == 0:  # if nwest border
            Wall(self, 0, 9, BLUE)  # draw wall at west door
        else:
            Door(self, 0, 9)  # draw west door

        if self.player.overworldcoords[0] == 2:  # if east border
            Wall(self, 31, 9, BLUE)  # draw wall at east door
        else:
            Door(self, 31, 9)  # draw east door

    def create_walls(self, map, color):
        self.doors.empty()
        self.blocks.empty()
        for x in map[0]:
            if x == 17:
                # perform check here instead
                # Door(self, x, 0) #draw north door
                # Door(self, x, 17) #draw south door
                self.door_or_walls()
            else:
                Wall(self, x, 0, color)  # draw north wall
                Wall(self, x, 17, color)  # draw south wall
        for y in map[1]:
            if y == 9:
                # Door(self, 0, y) #draw west door
                # Door(self, 31, y) #draw east door
                self.door_or_walls()
            else:
                Wall(self, 0, y, color)  # draw west wall
                Wall(self, 31, y, color)  # draw east wall
        for x in range(1, 31):
            for y in range(1, 17):
                self.bg = Background(self, x, y)
