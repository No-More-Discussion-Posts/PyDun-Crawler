import pygame
import sys
from .entities import *
from .config import *
import random




class Generate_dun():

    
    def DrawWalls(self, map):
        for x in map[0]:
            if x == 17:
                self.door = Door(self, x, 0)
                self.door = Door(self, x, 17)
            else:
                self.wall = Wall(self, x, 0)
                self.wall = Wall(self, x, 17)
        for y in map[1]:
            if y == 9:
                self.door = Door(self, 0, y)
                self.door = Door(self, 31, y)
            else:
                self.wall = Wall(self, 0, y)
                self.wall = Wall(self, 31, y)
        for x in range(1,31):
            for y in range(1,17):
                self.bg = Background(self, x, y)

