import random
from inventory import Inventory
import pygame as pg #TODO: make consistent

items = {1: 'S HP Pot', 2: 'M HP Pot', 3: 'L HP Pot'}



class Entity:

    def update(self):
        '''All entities need an update method to be called per game turn.'''
        pass

class Monster(Entity):
    def __init__(self,):
        pass

class Goblin(Monster):
    def __init__(self):
        self.name = 'Goblin'
        #self.game = game
        #self.lvl = int(game.turn * .25)
        self.max_hp = 10
        self.hp = 10
        self.atk = 1
        self.item = items[random.randint(1, 3)]
        
class HobGoblin(Monster):
    def __init__(self):
        self.name = 'HobGoblin'
        #self.game = game
        #self.lvl = int(game.turn * .25)
        self.max_hp = 15
        self.hp = 15
        self.atk = 2
        self.item = items[random.randint(1, 3)]

class Ogre(Monster):
    def __init__(self):
        self.name = 'Ogre'
        #self.game = game
        #self.lvl = int(game.turn * .25)
        self.max_hp = 20
        self.hp = 20
        self.atk = 4
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
        self.lvl = int(self.game.turn * .4)
        self.atk = self.atk
        self.hp = self.hp
        self.max_hp = self.max_hp
        #self.rect.x = self.x * 20
        #self.rect.y = self.y * 20

    @property
    def lvl(self):
        return self._lvl
    
    @lvl.setter
    def lvl(self, value):
        self._lvl = value
        self.max_hp = 20
        self.hp = self.max_hp
        self.atk = 2
    

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