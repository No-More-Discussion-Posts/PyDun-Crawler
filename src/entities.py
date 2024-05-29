import random
from inventory import Inventory
import pygame as pg #TODO: make consistent

items = {1: 'Health Potion', 2: 'Attack Potion', 3: 'Defense Potion'}



class Entity:

    def update(self):
        '''All entities need an update method to be called per game turn.'''
        pass

class Monster(Entity):
    def __init__(self,):
        pass

class Goblin(Monster):
    def __init__(self, game):
        self.name = 'Goblin'
        self.game = game
        self.lvl = int(game.turn * .25)
        self.max_hp = 5 + (1 * self.lvl)
        self.hp = 5 + (1 * self.lvl)
        self.atk = 1 + (1 * self.lvl)
        self.item = items[random.randint(1, 3)]

class Player(Entity):
    def __init__(self, name, game,x:int=0,y:int=0):
        self.name = name
        self.game = game
        self.lvl = int(game.turn * .4)
        #self.dex = 2 * lvl
        self.inventory = Inventory()
        # self.image = pg.surface()
        # self.image.fill((255,255, 0))
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
    def movement(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def update(self):
        self.lvl = int(self.game.turn)
        self.atk = self.atk
        #self.rect.x = self.x * 20
        #self.rect.y = self.y * 20

    @property
    def lvl(self):
        return self._lvl
    
    @lvl.setter
    def lvl(self, value):
        self._lvl = value
        self.max_hp = 20 + (2 * int(self.lvl * .1))
        self.hp = self.max_hp
        self.atk = 1 + (1 * int(self.lvl * .2))
    

def miss_hit(player_dex, enemy_dex):
    pdex = player_dex
    edex = enemy_dex
    if edex > pdex:
        miss_chance = int(100-((pdex/edex)*100))
    elif pdex > edex:
        miss_chance = 0
    if miss_chance == 0:
        return True
    elif miss_chance >= 100:
        return False
    elif 100 > miss_chance > 0:
        y = random.randint(1, 100)
        if y > miss_chance:
            return True
        elif y < miss_chance:
            return False
        
class Wall():
    def __init__(self, game, x, y) -> None:
        pass

    def move():
        pass

class Door():
    def __init__(self, game, x, y) -> None:
        pass

class Treasure():
    def __init__(self, game, x, y) -> None:
        pass