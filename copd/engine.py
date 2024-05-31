import pygame
import sys
from .entities import *
from .menus import PauseMenu, BattleMenu
from .config import *
from random import randint


class Engine:
    def __init__(self):
        self.turn = 0
        self.running = False
        # self.player = Player("Bilbo",self) # TODO: Character creation?
        # self.enemies = pygame.sprite.LayeredUpdates()
        self.enemies = []

    def update(self):
        """Make updates every turn such as monster movement, etc.
        Initiated by player movement/action in battle.
        """
        #self.turn += 1
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

    def handle_event(self,event):
        """Manage events such as keypress, mouse clicks, etc."""
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                PauseMenu(self)
                self.draw()
            #if event.key == pygame.K_b:
                #BattleMenu(self)  -Testing -Roland
            if event.key == pygame.K_w:
                #Moves player incriments 
                self.player.movement(0, -1)
                #checks for player and wall overlap
                #if true, moves player back 1
                self.player.check_collisions(0, 1)
                self.turn += 1
                self.draw()
                self.monster.movement(self.player)
                self.player.check_collisions(0, 1)
                self.draw()
            if event.key == pygame.K_s:
                self.player.movement(0, 1)
                self.player.check_collisions(0, -1)
                self.turn += 1
                self.draw()
                self.monster.movement(self.player)
                self.player.check_collisions(0, -1)
                self.draw()
            if event.key == pygame.K_a:
                self.player.movement(-1, 0)
                self.player.check_collisions(1, 0)
                self.turn += 1
                self.draw()
                self.monster.movement(self.player)
                self.player.check_collisions(1, 0)
                self.draw()
            if event.key == pygame.K_d:
                self.player.movement(1, 0)
                self.player.check_collisions(-1, 0)
                self.turn += 1
                self.draw()
                self.monster.movement(self.player)
                self.player.check_collisions(-1, 0)
                self.draw()

    def new_game(self):
        #initialize all sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.monsters = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        #create player character
        self.player = Player("Bilbo", self, 15, 9)
        #draws Wall Entitiy at top and bottom of tile_map in config
        for x in tile_map[0]:
            self.wall = Wall(self, x, 0)
            self.wall = Wall(self, x, 17)
        #draws Wall Entitiy at leftmost and rightmost positions of tile_map in config
        #add doors to each wall edge!!!!!!!!!!!!! -Roland
        for y in tile_map[1]:
            self.wall = Wall(self, 0, y)
            self.wall = Wall(self, 31, y)
        #draws background Entity in each tile of Tile_map in config
        #placed in lowest layer
        for x in range(1,31):
            for y in range(1,17):
                self.bg = Background(self, x, y)


        self.door = Door(self, 0, 7)


        #initilizes random enemy sprite in room
        num = random.randint(1, 3)
        if num == 1:
            self.monster = Goblin(self)
        if num == 2:
            self.monster = HobGoblin(self)
        if num == 3:
            self.monster = Ogre(self)

    def draw(self):
        """Draw to the screen"""
        #update "all sprites", then draw to screem
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        #update player sprites and draws to screen
        self.players.update()
        self.players.draw(self.screen)
        #updates and draws non-traversable sprites
        self.blocks.update()
        self.blocks.draw(self.screen)
        #displays turn to screen
        self.show_turn()
        #updates mosnster sprite groups and draws to screen
        self.monsters.update()
        self.monsters.draw(self.screen)

        self.doors.update()
        self.doors.draw(self.screen)
        #self.Test_Grid()
        #updates all updates//draws to pygame screen
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