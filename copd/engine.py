import pygame
import random
import sys

from .entities import *
# from .menus import PauseMenu, BattleMenu
from .config import DEFAULT_MAP
from .states import GameStates
from .input_handlers import EventHandler
#test
from .manager.systems import Movement
from .manager.components import Position,Velocity



class Engine:
    
    def __init__(self):
        self.turn = 0
        self.running = False
        self.state = GameStates.MAIN # will need to change this when changing between menus
        self.enemies = []
        self.event_handler = EventHandler(self)
        self.handle_event = self.event_handler.handle_event
        self.movement = Movement()



    def add_player(self,player = None)-> None:
        #initilize player object
        if player is None:
            self.player = Player("Bilbo", self, 15, 9)
            self.player.add_component(Position(15,9))
            self.player.add_component(Velocity())
            self.movement.add_entity(self.player)
        else:
            self.player = player
        self.movement.add_entity(self.player)

    def load_map(self, map = None)->None:
        # if no map is supplied in args
        if map is not None:
            map = map
        else:
            #load default starting map
            map = DEFAULT_MAP


        #draws Wall Entitiy at top and bottom of tile_map in config
        for x in map[0]:
            self.wall = Wall(self, x, 0)
            self.wall = Wall(self, x, 17)
        #draws Wall Entitiy at leftmost and rightmost positions of tile_map in config
        #add doors to each wall edge!!!!!!!!!!!!! -Roland
        for y in map[1]:
            self.wall = Wall(self, 0, y)
            self.wall = Wall(self, 31, y)
        #draws background Entity in each tile of Tile_map in config
        #placed in lowest layer
        for x in range(1,31):
            for y in range(1,17):
                self.bg = Background(self, x, y)
        self.door = Door(self, 1, 7)

    def add_monster(self,monster = None):
        if monster is not None:
            self.monster = monster
        else:
            #initilizes random enemy sprite in room
            num = random.randint(1, 3)
            if num == 1:
                self.monster = Goblin(self)
            if num == 2:
                self.monster = HobGoblin(self)
            if num == 3:
                self.monster = Ogre(self)
        self.movement.add_entity(self.monster)

    def new_game(self):
        #initialize all sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.monsters = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        #create player character

    def update(self):
        """Make updates every turn such as monster movement, etc.
        Initiated by player movement/action in battle.
        """
        #updates all sprite object values
        self.all_sprites.update()
        self.players.update()
        self.blocks.update()
        self.monsters.update()
        self.doors.update()
        self.draw()

    def draw(self):
        """Draw to the screen"""
        #draws all aprite groups to screen
        self.all_sprites.draw(self.screen)
        self.players.draw(self.screen)
        self.blocks.draw(self.screen)
        self.monsters.draw(self.screen)
        self.doors.draw(self.screen)
        self.show_turn()

        pygame.display.update()

    def show_turn(self):
        #displays turn counter
        font = pygame.font.get_default_font()
        FONT = pygame.font.Font(font, TILE_SIZE)
        turn = FONT.render(str(self.turn), False, "black")
        self.screen.blit(turn, (20, 20))
        # self.screen.blit(turn,(TILE_SIZE*2,SCREEN_WIDTH-(TILE_SIZE*2)))

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_CAPTION)
        self.draw()

        self.running = True
        while self.running:
            # SHOULD WAIT FOR INPUT
            for event in pygame.event.get():
                self.handle_event(event)
            #self.draw()
        pygame.quit()
        sys.exit()

    def Test_Grid(self):

        for x in range(0, 640, 20):
            pygame.draw.line(self.screen, (128, 128, 128), (x, 0), (x, 360))
        # draw lines vertically
        for y in range(0, 360, 20):
            pygame.draw.line(self.screen, (128, 128, 128), (0, y), (640, y))