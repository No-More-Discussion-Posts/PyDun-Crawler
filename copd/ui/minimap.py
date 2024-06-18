import pygame
from copy import deepcopy as copy
from copd.config import *

class MiniMap():
    def __init__(self,game):
        ''' 0,0 1,0 2,0
            0,1 1,1 2,1
            0,2 1,2 2,2'''
        
        self.game = game
        self.visited = []
        self.canvas = pygame.Surface((3*TILE_SIZE,3*TILE_SIZE))
        self.canvas.set_alpha(100)

    @property
    def location(self):
        return self.game.player.overworldcoords
    
    def visit(self,loc):
        # should have check for loc being a tuple of depth 2
        if loc not in self.visited:
            self.visited.append(copy(loc)) 
        if self.game.debug:
            print("Visited: \n")
            print(self.visited)

    def draw(self):
        self.canvas.fill(Colors.BLACK)
        color = None
        for x in range(3):
            for y in range(3):
                color = Colors.BLACK
                if [x,y] == self.location:
                    # if self.game.debug:
                    #   print(f"player loc: {self.location}\nLoc: {x,y}")
                    color = Colors.NachoCheese
                elif [x,y] in self.visited:
                    color = Colors.WHITE
                pygame.draw.rect(self.canvas,color,[x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE],width=0)
        self.game.screen.blit(self.canvas,(SCREEN_WIDTH-(TILE_SIZE*4),TILE_SIZE))



    def update(self):
        ...
