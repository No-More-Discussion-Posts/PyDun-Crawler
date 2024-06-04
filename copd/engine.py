import pygame
import random
import sys

from .entities import *
from .menus import PauseMenu, BattleMenu
from .config import DEFAULT_MAP
from .ecs.states import GameStates
from .input_handlers import EventHandler
#test
from .ecs.systems import Movement, Collision, Turn
from .ecs.components import Position,Velocity, TurnCounter




#test
class Engine:
    
    def __init__(self):
        self.components = {}
        self.Turn = Turn()
        self.running = False
        self.state = GameStates.MAIN # will need to change this when changing between menus
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

    def add_component(self,component):
        self.components[type(component)] = component
    
    def get(self,component):
        return self.components.get(component)

    def add_player(self,player = None)-> None:
        #initilize player object
        if player is None:
            self.player = Player("Bilbo", self, 15, 9)
            self.player.add_component(Position(15,9))
            self.player.add_component(Velocity())
        else:
            self.player = player
        self.Movement.add_entity(self.player)
        self.Collision.add_entity(self.player)

    def load_start_map(self, color ,map = None)->None:
        # if no map is supplied in args
        if map is not None:
            map = map
        else:
            #load default starting map
            map = DEFAULT_MAP
        self.add_player()
        self.add_monster()
        self.DrawWalls(map, color)
        self.add_treasure(14, 10)

    def load_map(self, color, map = None)->None:
        
        if map is not None:
            map = map
        else:
            map = DEFAULT_MAP
        pygame.sprite.Group.empty(self.blocks)
        self.monster.kill()
        self.add_monster()
        self.DrawWalls(map, color)
        self.add_treasure(14, 10)
        
    def update(self):
        pass
        #self.Turn.update()
        
    #     self.turn += 1
    #     """Make updates every turn such as monster movement, etc.
    #     Initiated by player movement/action in battle.
    #     """
    #     #updates all sprite object values
    #     self.all_sprites.update()
    #     self.players.update()
    #     # self.blocks.update()
    #     self.monsters.update()
    #     self.doors.update()
    #     self.draw()

    def draw(self):
        """Draw to the screen"""
        #draws all aprite groups to screen
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
        #displays turn counter
        font = pygame.font.get_default_font()
        FONT = pygame.font.Font(font, TILE_SIZE)
        turn = FONT.render(str(self.get(TurnCounter).turn), False, "black")
        self.screen.blit(turn, (20, 20))
        # self.screen.blit(turn,(TILE_SIZE*2,SCREEN_WIDTH-(TILE_SIZE*2)))
    
    def show_location(self):
        #displays turn counter
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
                BattleMenu(self)
            self.draw()
        pygame.quit()
        sys.exit()

    def Test_Grid(self):

        for x in range(0, 640, 20):
            pygame.draw.line(self.screen, (128, 128, 128), (x, 0), (x, 360))
        # draw lines vertically
        for y in range(0, 360, 20):
            pygame.draw.line(self.screen, (128, 128, 128), (0, y), (640, y))


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

    def add_treasure(self, x, y):
        self.treasure = Treasure(self, x, y)
    """ 
    def WestWall(self, map, color):
        for y in map[1]:
            if y == 9:
                self.door = Door(self, 0, y) #draw west door
            
    
    def EastWall(self, map, color):
        for y in map[1]:
            if y == 9:
                self.door = Door(self, 31, y) #draw east door

    def NorthWall(self, map, color):
        pass
    
    def SouthWall(self, map, color):
        pass
    """
    
    def DrawWalls(self, map, color):
        for x in map[0]:
            if x == 17:
                #if map[0] 
                self.door = Door(self, x, 0) #draw north door
                self.door = Door(self, x, 17) #draw south door
            else:
                self.wall = Wall(self, x, 0, color) #draw north wall
                self.wall = Wall(self, x, 17, color) #draw south wall
        for y in map[1]:
            if y == 9:
                self.door = Door(self, 0, y) #draw west door
                self.door = Door(self, 31, y) #draw east door
            else:
                self.wall = Wall(self, 0, y, color) #draw west wall
                self.wall = Wall(self, 31, y, color) #draw east wall
        for x in range(1,31):
            for y in range(1,17):
                self.bg = Background(self, x, y)