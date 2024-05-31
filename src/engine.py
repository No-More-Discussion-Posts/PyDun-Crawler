import pygame
import sys
from entities import *
from menus import PauseMenu, BattleMenu
from config import *


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
        self.turn += 1
        self.player.update()
        # for enemy in self.enemies:
        #      enemy.update()

    def events(self):
        """Manage events such as keypress, mouse clicks, etc."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PauseMenu(self)
                if event.key == pygame.K_b:
                    BattleMenu(self)
                if event.key == pygame.K_w:
                    #Moves player incriments 
                    self.player.movement(0, -1)
                    #checks for player and wall overlap
                    #if true, moves player back 1
                    self.player.check_collisions(0, 1)
                if event.key == pygame.K_s:
                    self.player.movement(0, 1)
                    self.player.check_collisions(0, -1)
                if event.key == pygame.K_a:
                    self.player.movement(-1, 0)
                    self.player.check_collisions(1, 0)
                if event.key == pygame.K_d:
                    self.player.movement(1, 0)
                    self.player.check_collisions(-1, 0)

    def new_game(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.player = Player("bilbo", self, 17, 9)
        for x in tile_map[0]:
            self.wall = Wall(self, x, 0)
            self.wall = Wall(self, x, 17)
        for y in tile_map[1]:
            self.wall = Wall(self, 0, y)
            self.wall = Wall(self, 31, y)

    def draw(self):
        """Draw to the screen"""
        self.screen.fill("white")
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.blocks.update()
        self.blocks.draw(self.screen)
        self.Test_Grid()
        self.show_turn()

        pygame.display.update()

    def show_turn(self):
        font = pygame.font.get_default_font()
        FONT = pygame.font.Font(font, TILE_SIZE)
        turn = FONT.render(str(self.turn), False, "black")
        self.screen.blit(turn, (20, 20))
        # self.screen.blit(turn,(TILE_SIZE*2,SCREEN_WIDTH-(TILE_SIZE*2)))

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_CAPTION)

        self.running = True
        while self.running:
            # SHOULD WAIT FOR INPUT
            self.events()
            self.draw()
        pygame.quit()
        sys.exit()

    def Test_Grid(self):

        for x in range(0, 640, 20):
            pygame.draw.line(self.screen, (128, 128, 128), (x, 0), (x, 360))
        # draw lines vertically
        for y in range(0, 360, 20):
            pygame.draw.line(self.screen, (128, 128, 128), (0, y), (640, y))
