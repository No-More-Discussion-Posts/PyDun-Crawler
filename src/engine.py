import pygame
import sys
from entities import Player
from menus import PauseMenu,BattleMenu
from config import *
class Engine:
    def __init__(self):
        self.turn = 0
        self.running = False
        self.player = Player("Bilbo",1,self) # TODO: Character creation?
        # self.enemies = pygame.sprite.LayeredUpdates()
        self.enemies = []

    def update(self):
        '''Make updates every turn such as monster movement, etc. 
           Initiated by player movement/action in battle.
        '''
        self.turn += 1
        # self.player.update()
        # for enemy in self.enemies:
        #      enemy.update()

    def events(self):
        '''Manage events such as keypress, mouse clicks, etc.''' 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PauseMenu(self)
                if event.key == pygame.K_b:
                    BattleMenu(self)

    def draw(self):
        '''Draw to the screen'''
        self.screen.fill('white')
        self.Test_Grid()
        self.show_turn()
        pygame.display.update()

    def show_turn(self):
        font = pygame.font.get_default_font()
        FONT = pygame.font.Font(font,TILE_SIZE)
        turn = FONT.render(str(self.turn),False,'black')
        self.screen.blit(turn,(20,20))
        # self.screen.blit(turn,(TILE_SIZE*2,SCREEN_WIDTH-(TILE_SIZE*2)))

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_CAPTION)
        self.running=True
        while self.running:
            self.events()
            self.draw()
        pygame.quit()
        sys.exit()

    def Test_Grid(self):
        # draw red rectangle
        pygame.draw.rect(self.screen, (255, 0, 0), [100, 50, 400, 100], 6)

        #draw lines horizontally
        for x in range(0, 640, 20):
                pygame.draw.line(self.screen, (128, 128, 128), (x, 0), (x, 360))
        #draw lines vertically
        for y in range(0, 360, 20):
                pygame.draw.line(self.screen, (128, 128, 128), (0, y), (640, y))
        #draw blue rectangle
        pygame.draw.rect(self.screen, (0, 0, 255), [50, 100, 400, 100], 6)