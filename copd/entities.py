import random
import math
from .inventory import Inventory, Equipped
import pygame as pg  # TODO: make consistent
from .config import *
from .menus import BattleMenu
import time
from .ecs.components import Position,Velocity

items = {1: "S HP Pot", 2: "M HP Pot", 3: "L HP Pot"}

class immovable_entitiy(pg.sprite.Sprite):
    #class to initilize a sprite that is immovable
    pass
class Entity(pg.sprite.Sprite):
    def __init__(self,game,x=0,y=0):
        super().__init__()
        self.components = {}
        self.add_component(Position(x,y))
        self.add_component(Velocity())

    @property
    def x(self):
        return self.get(Position).x
    
    @x.setter
    def x(self,x):
        self.get(Position).x = x

    @property 
    def y(self):
        return self.get(Position).y
    
    @y.setter
    def y(self,y):
        self.get(Position).y = y
        
    #class to initilize a sprite with movement and actions
    def update(self):
        """All entities need an update method to be called per game turn."""
        pass

    def add_component(self,component):
        self.components[type(component)] = component
    
    def get(self,component):
        return self.components.get(component)
    
    def movement(self):
        #updates sprite x and y coords
        self.game.update()
        dx = self.get(Velocity).dx * TILE_SIZE
        dy = self.get(Velocity).dy * TILE_SIZE
        self.rect.move_ip(dx,dy)

class Monster(Entity):

    def __init__(self, game, x=0, y=0):
        super().__init__(game, x, y)
        self.add_component(Position(x,y))
        self.add_component(Velocity())

    def sprite_gen(self):
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

    def movement(self):
        #enemy to player vector math here
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
        if(abs(dx) < 100) and (abs(dy) < 100):
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
        # time.sleep(.5) if velocity > 0
        self.rect.x = self.x
        self.rect.y = self.y
        self.monster_rect = pg.Rect(self.rect.x, self.rect.y, TILE_SIZE, TILE_SIZE)

class Goblin(Monster):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Goblin"
        self.game = game
        self._layer = Player_Layer
        # self.lvl = int(game.turn * .25)
        self.max_hp = 10
        self.hp = 10
        self.atk = 1
        self.item = items[random.randint(1, 3)]
        self.sprite_gen()

class HobGoblin(Monster):
    def __init__(self, game):
        super().__init__(game)
        self.name = "HobGoblin"
        self.game = game
        self._layer = Player_Layer
        # self.lvl = int(game.turn * .25)
        self.max_hp = 15
        self.hp = 15
        self.atk = 2
        self.item = items[random.randint(1, 3)]
        self.sprite_gen()

class Ogre(Monster):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Ogre"
        self.game = game
        self._layer = Player_Layer
        # self.lvl = int(game.turn * .25)
        self.max_hp = 20
        self.hp = 20
        self.atk = 4
        self.item = items[random.randint(1, 3)]
        self.sprite_gen()
    
class Player(Entity):
    def __init__(self, name, game, x, y):
        super().__init__(game,x,y)
        #name of player
        self.name = name
        #current running game
        self.game = game
        self._layer = Player_Layer
        self.lvl = int(game.turn * 0.4)
        # self.dex = 2 * lvl
        self.inventory = Inventory()
        self.equipped = Equipped()

        self.groups = self.game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        #
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(BreastCancerAwareness)

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

        self.components = {}



    def update(self):
        self.lvl = int(self.game.turn * 0.4)
        self.atk = self.atk
        self.hp = self.hp
        self.max_hp = self.max_hp
    
    
            
    @property
    def lvl(self):
        return self._lvl

    @lvl.setter
    def lvl(self, value):
        self._lvl = value
        self.max_hp = 20
        self.hp = self.max_hp
        self.atk = 2

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        ###WALL SPECIFIC###
        self._layer = Tile_Layer
        self.groups = self.game.blocks
        ###WALL SPECIFIC###
        pg.sprite.Sprite.__init__(self, self.groups)

        #sprite size(used for referencing the sprite)
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        ###WALL SPECIFIC###
        self.image.fill(BLUE)
        ###WALL SPECIFIC###

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
class Door(Entity): 
    def __init__(self, game, x, y):
        super().__init__(game,x,y)
        self.game = game
        self._layer = Door_Layer
        self.groups = self.game.doors
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(Snugglepuss)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Treasure():
    def __init__(self, game, x, y) -> None:
        pass

###TYLER EXPERIMENTAL###
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
###TYLER EXPERIMENTAL###