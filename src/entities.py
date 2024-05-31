import random
import math
from inventory import Inventory
import pygame as pg  # TODO: make consistent
from config import *
from menus import *

items = {1: "S HP Pot", 2: "M HP Pot", 3: "L HP Pot"}


class Entity(pg.sprite.Sprite):
    def update(self):
        """All entities need an update method to be called per game turn."""
        pass


class Monster(Entity):
    def __init__(self, game):
        self.game = game

    def movement(self,player):
        self.game.update()
        self.player = player
        #enemy to player vector math here
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        if(abs(dx) > abs(dy)):
            if(dx > 0):
                dx = 1
                self.x += dx * TILE_SIZE
            elif(dx < 0):
                dx = -1
                self.x += dx * TILE_SIZE
        else:
            if(dy > 0):
                dy = 1
                self.y += dy * TILE_SIZE
            elif(dy < 0):
                dy = -1
                self.y += dy * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.monster_rect = pg.Rect(self.rect.x, self.rect.y, TILE_SIZE, TILE_SIZE)

class Goblin(Monster):
    def __init__(self, game):
        self.name = "Goblin"
        self.game = game
        # self.lvl = int(game.turn * .25)
        self.max_hp = 10
        self.hp = 10
        self.atk = 1
        self.item = items[random.randint(1, 3)]

        #Sprite Generation Block
        self.groups = self.game.monsters
        pg.sprite.Sprite.__init__(self, self.groups)
        #random location on grid
        self.x = random.randint(1,30) * TILE_SIZE
        self.y = random.randint(1,16) * TILE_SIZE
        #rest of sprite generation block
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pg.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #end sprite generation block



class HobGoblin(Monster):
    def __init__(self, game):
        self.name = "HobGoblin"
        self.game = game
        # self.lvl = int(game.turn * .25)
        self.max_hp = 15
        self.hp = 15
        self.atk = 2
        self.item = items[random.randint(1, 3)]

        #Sprite Generation Block
        self.groups = self.game.monsters
        pg.sprite.Sprite.__init__(self, self.groups)
        #random location on grid
        self.x = random.randint(1,30) * TILE_SIZE
        self.y = random.randint(1,16) * TILE_SIZE
        #rest of sprite generation block
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pg.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #end sprite generation block
    


class Ogre(Monster):
    def __init__(self, game):
        self.name = "Ogre"
        self.game = game
        # self.lvl = int(game.turn * .25)
        self.max_hp = 20
        self.hp = 20
        self.atk = 4
        self.item = items[random.randint(1, 3)]

        #Sprite Generation Block
        self.groups = self.game.monsters
        pg.sprite.Sprite.__init__(self, self.groups)
        #random location on grid
        self.x = random.randint(1,30) * TILE_SIZE
        self.y = random.randint(1,16) * TILE_SIZE
        #rest of sprite generation block
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pg.Surface([self.width, self.height])
        self.image.fill(DaytonaPeach)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #end sprite generation block
    


class Player(Entity):
    def __init__(self, name, game, x, y):
        self.name = name
        self.game = game
        self._layer = Player_Layer
        self.lvl = int(game.turn * 0.4)
        # self.dex = 2 * lvl
        self.inventory = Inventory()

        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(BreastCancerAwareness)

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

    def movement(self, dx, dy):
        self.game.update()
        self.x += dx * TILE_SIZE
        self.y += dy * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.player_rect = pg.Rect(self.rect.x, self.rect.y, TILE_SIZE, TILE_SIZE)

    def update(self):
        self.lvl = int(self.game.turn * 0.4)
        self.atk = self.atk
        self.hp = self.hp
        self.max_hp = self.max_hp
        # self.rect.x = self.x * TILE_SIZE
        # self.rect.y = self.y * TILE_SIZE
    
    def check_collisions(self, x, y):
        #checks the player sprite(self) and and sprite in the blocks sprite group or overlap
        if pg.sprite.spritecollide(self, self.game.blocks, False):
            #if there is overlap between player and wall sprites, the player the designated spot
            self.movement(x, y)
        elif pg.sprite.spritecollide(self, self.game.monsters, False):
            BattleMenu(self.game)

    @property
    def lvl(self):
        return self._lvl

    @lvl.setter
    def lvl(self, value):
        self._lvl = value
        self.max_hp = 20
        self.hp = self.max_hp
        self.atk = 2


"""
class Player(pg.sprite.Sprite):
    def __init__(self, game, x , y):
        
        self.game = game
        self._layer = Player_Layer
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x + TILE_SIZE
        self.y = y + TILE_SIZE
        self.width = TILE_SIZE
        self.hieght = TILE_SIZE

        self.image = pg.Surface([self.width, self.hieght])
        self.image.fill(DeadSalmon)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y    
    
    
    def update(self):
        pass
"""


def miss_hit(player_dex, enemy_dex):
    pdex = player_dex
    edex = enemy_dex
    if edex > pdex:
        miss_chance = int(100 - ((pdex / edex) * 100))
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


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = Tile_Layer
        self.groups = self.game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.wall_rect = pg.Rect(self.rect.x, self.rect.y, TILE_SIZE, TILE_SIZE)

class Background(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = Tile_Layer
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(MasterChief)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Door:
    def __init__(self, game, x, y) -> None:
        pass


class Treasure:
    def __init__(self, game, x, y) -> None:
        pass
