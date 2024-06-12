import random
import math
from .inventory import Inventory, Equipped
import pygame as pg  # TODO: make consistent
from .config import *
from .menus import BattleMenu
import time
from .engine.components import Position, Velocity


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
    def __init__(self, game, x=0, y=0):
        super().__init__()
        self.components = {}
        self.game = game
        self.add_component(Position(x, y))
        self.add_component(Velocity())
        self.stun = 0

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

    def __init__(self, game, x=0, y=0):
        super().__init__(game, x, y)
        self.stun = 0

    def sprite_gen(self, color=None):
        # Sprite Generation Block
        self.groups = self.game.monsters
        pg.sprite.Sprite.__init__(self, self.groups)
        # random location on grid
        self.x = random.randint(1, 30) * TILE_SIZE
        self.y = random.randint(1, 16) * TILE_SIZE
        # rest of sprite generation block
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pg.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
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
        self._layer = Player_Layer
        # self.lvl = int(game.turn * .25)
        self.max_hp = 10
        self.hp = 10
        self.atk = 1
        self.dex = 2
        self.item = items[random.randint(1, 4)]
        self.sprite_gen(BLACK)
        # self.image.fill(BLACK)


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
        self.dex = 1
        self.item = items[random.randint(1, 4)]
        self.sprite_gen(GREEN)
        # self.image.fill(GREEN)


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
        self.dex = 0
        self.item = items[random.randint(1, 4)]
        self.sprite_gen(RED)
        # self.image.fill(RED)


class Player(Entity):
    def __init__(self, name, game, x, y):
        super().__init__(game, x, y)
        # name of player
        self.name = name
        # current running game
        self._layer = Player_Layer
        self.max_hp = 20
        self.hp = 20
        self.atk = 2
        self.dex = 2
        self.inventory = Inventory()
        self.equipped = Equipped()

        self.groups = self.game.players
        pg.sprite.Sprite.__init__(self, self.groups)

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(BreastCancerAwareness)

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

        self.overworldcoords = [1, 1]  # overworld coordinates. starts at 1,1


class Wall(Entity):
    def __init__(self, game, x, y, color):
        super().__init__(game, x, y)
        ###WALL SPECIFIC###
        self._layer = Tile_Layer
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
        self._layer = Tile_Layer
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.add_component(Position(x, y))
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(MasterChief)

        self.rect = self.image.get_rect()
        self.rect.x = self.get(Position).x * TILE_SIZE
        self.rect.y = self.get(Position).y * TILE_SIZE


class Door(Entity):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
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
        self.rect.x = self.get(Position).x * TILE_SIZE
        self.rect.y = self.get(Position).y * TILE_SIZE


class Treasure(Entity):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self._layer = Door_Layer
        self.groups = self.game.treasures
        pg.sprite.Sprite.__init__(self, self.groups)

        self.item = items[random.randint(1, 4)]

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pg.Surface([self.width, self.height])
        self.image.fill(NachoCheese)

        self.rect = self.image.get_rect()
        self.rect.x = self.get(Position).x * TILE_SIZE
        self.rect.y = self.get(Position).y * TILE_SIZE
