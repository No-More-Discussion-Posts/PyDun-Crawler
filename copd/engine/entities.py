import random
import math
import os
import csv
from copd.engine.inventory import Inventory, Equipped
import pygame as pg  # TODO: make consistent
from copd.config import *
import time
from copd.engine.components import Position, Velocity, Flag


items = {
    1: "Health Pot",
    2: {"Helm": "Bronze Helmet"},
    3: {"Armor": "Bronze Armor"},
    4: {"Weapon": "Bronze Sword"},
}


class immovable_entitiy(pg.sprite.Sprite):
    # class to initilize a sprite that is immovable
    pass

class Entity(pg.sprite.Sprite):
    def __init__(self, game, x=0, y=0,group=None,name=None):
        super().__init__()
        self.components = {}

        self.game = game
        self.add_component(Position(x, y))
        self.add_component(Velocity())
        self.stun = 0
        self.image = game.tile_map.get_image(name)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
        # if filename is not None:
        #     img = pg.image.load(filename).convert_alpha()
        #     self.image.blit(img,(0,0))
            
           
        if group is not None:
            pg.sprite.Sprite.__init__(self, group)
        

    @property
    def x(self):
        return self.rect.x
    
    @property
    def y(self):
        return self.rect.y
    
    @x.setter
    def x(self,x):
        self.rect.x = x

    @y.setter
    def y(self,y):
        self.rect.y = y
    def update(self):
        self.draw()

    def draw(self):
        self.game.screen.blit(self.image,(self.x,self.y))

    # class to initilize a sprite with movement and actions

    def add_component(self, component):
        self.components[type(component)] = component

    def get(self, component):
        return self.components.get(component)

    def movement(self):
        # updates sprite x and y coords

        dx = self.get(Velocity).dx * TILE_SIZE
        dy = self.get(Velocity).dy * TILE_SIZE
        self.rect.move_ip(dx, dy)


class Monster(Entity):

    def __init__(self, game, x=0, y=0,name=None):
        super().__init__(game, x, y,game.monsters,name=name)
        self.x = random.randint(1, X_TILES-1) * TILE_SIZE
        self.y = random.randint(1, Y_TILES-1) * TILE_SIZE
        self.in_combat = Flag(False)
        self.stun = 0

    def sprite_gen(self, color=None):
        # Sprite Generation Block
        # self.groups = self.game.monsters
        # pg.sprite.Sprite.__init__(self, self.groups)
        # # random location on grid
        
        # rest of sprite generation block
        # self.width = TILE_SIZE
        # self.height = TILE_SIZE
        # self.image = pg.Surface([self.width, self.height])
        # self.rect = self.image.get_rect()
        # self.rect.x = self.x
        # self.rect.y = self.y
        if color != None:
            self.image.fill(color)
        # end sprite generation block

    def movement(self):
        # enemy to player vector math here
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
        if (abs(dx) < 100) and (abs(dy) < 100):
            if abs(dx) > abs(dy):
                if dx > 0:
                    dx = 1
                    self.x += dx * TILE_SIZE
                elif dx < 0:
                    dx = -1
                    self.x += dx * TILE_SIZE
            else:
                if dy > 0:
                    dy = 1
                    self.y += dy * TILE_SIZE
                elif dy < 0:
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
        self._layer = Layers.Player_Layer
        # self.lvl = int(game.turn * .25)
        self.max_hp = 10
        self.hp = 10
        self.atk = 1
        self.dex = 2
        self.item = items[random.randint(1, 4)]
        self.sprite_gen(Colors.BLACK)
        # self.image.fill(Colors.BLACK)


class HobGoblin(Monster):
    def __init__(self, game):
        super().__init__(game)
        self.name = "HobGoblin"
        self.game = game
        self._layer = Layers.Player_Layer
        # self.lvl = int(game.turn * .25)
        self.max_hp = 15
        self.hp = 15
        self.atk = 2
        self.dex = 1
        self.item = items[random.randint(1, 4)]
        self.sprite_gen(Colors.GREEN)
        # self.image.fill(Colors.GREEN)


class Ogre(Monster):
    def __init__(self, game):
        super().__init__(game,name='monster')
        self.name = "Ogre"
        self.game = game
        self._layer = Layers.Player_Layer
        # self.lvl = int(game.turn * .25)
        self.max_hp = 20
        self.hp = 20
        self.atk = 4
        self.dex = 0
        self.item = items[random.randint(1, 4)]


class Player(Entity):
    def __init__(self, name, game, x, y,filename=None):
        super().__init__(game, x*TILE_SIZE, y*TILE_SIZE,game.players,filename)
        self.in_combat = Flag(False)
        # name of player
        self.name = name
        # current running game
        self._layer = Layers.Player_Layer
        self.max_hp = 20
        self.hp = 20
        self.atk = 2
        self.dex = 2
        self.inventory = Inventory()
        self.equipped = Equipped()
        print(f"Player at: {self.x},{self.y}")
        # self.groups = self.game.players
        # pg.sprite.Sprite.__init__(self, self.groups)

        # self.width = TILE_SIZE
        # self.height = TILE_SIZE

        # self.image = pg.Surface([self.width, self.height])
        # self.image.fill(Colors.BreastCancerAwareness)

        # self.rect = self.image.get_rect()
        # self.rect.x = x * TILE_SIZE
        # self.rect.y = y * TILE_SIZE

        self.overworldcoords = [1, 1]  # overworld coordinates. starts at 1,1


class Wall(Entity):
    def __init__(self, game, x, y, color):
        super().__init__(game, x, y)
        ###WALL SPECIFIC###
        self._layer = Layers.Tile_Layer
        self.groups = self.game.blocks
        ###WALL SPECIFIC###
        pg.sprite.Sprite.__init__(self, self.groups)

        # sprite size(used for referencing the sprite)
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        ###WALL SPECIFIC###
        self.image.fill(color)
        ###WALL SPECIFIC###

        self.rect = self.image.get_rect()
        self.rect.x = self.get(Position).x * TILE_SIZE
        self.rect.y = self.get(Position).y * TILE_SIZE
        self.wall_rect = pg.Rect(self.rect.x, self.rect.y, TILE_SIZE, TILE_SIZE)


class Background(Entity):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self._layer = Layers.Tile_Layer
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.add_component(Position(x, y))
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(Colors.MasterChief)

        self.rect = self.image.get_rect()
        self.rect.x = self.get(Position).x * TILE_SIZE
        self.rect.y = self.get(Position).y * TILE_SIZE


class Door(Entity):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.game = game
        self._layer = Layers.Door_Layer
        self.groups = self.game.doors
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(Colors.Snugglepuss)

        self.rect = self.image.get_rect()
        self.rect.x = self.get(Position).x * TILE_SIZE
        self.rect.y = self.get(Position).y * TILE_SIZE


class Treasure(Entity):
    def __init__(self, game, x, y):
        super().__init__(game, x, y,group=game.treasures,name='chest')
        self._layer = Layers.Door_Layer

        self.item = items[random.randint(1, 4)]

