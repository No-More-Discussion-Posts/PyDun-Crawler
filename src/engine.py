import pygame
from entities import Player
from menus import PauseMenu,BattleMenu
from config import *
class Engine:
    def __init__(self):
        self.turn = 0
        self.running = False
        self.player = Player("Bilbo",1) # TODO: Character creation?
        pygame.display.set_caption(GAME_CAPTION)
        # self.enemies = pygame.sprite.LayeredUpdates()
        self.listening = []

    def update(self):
        '''Make updates every turn such as monster movement, etc. 
           Initiated by player movement/action in battle.
        '''
        self.turn += 1
        for listener in self.listening:
            listener.next_turn() # Maybe worth adding the current turn since creatures could be added later in the game.

    def events(self):
        '''Manage events such as keypress, mouse clicks, etc.'''
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PauseMenu(self)
                if event.key == pygame.K_b:
                    BattleMenu(self)

    def draw(self):
        '''Draw to the screen'''
        self.screen.fill('white')
        self.Test_Grid()
        pygame.display.flip()
    
    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.running=True
        while self.running:
            self.events()
            self.draw()


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