import random
import math
import os
import csv
from copd.engine.inventory import Inventory, Equipped
import pygame as pg  # TODO: make consistent
from copd.config import *
import time
from copd.engine.components import Position, Velocity, Flag
from random import randint


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
    def __init__(self, game, x=0, y=0, group=None, name=None, max_hp=0, atk=0, dex=0):
        super().__init__()
        self.components = {}
        self.name = name
        self.game = game
        self.add_component(Position(x, y))
        self.add_component(Velocity())
        self.stun = 0
        self.facing = "down"
        self.image = game.tile_map.get_image(name)
        self.rect = self.image.get_rect()
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        # these and maybe others add to a living entities subclass for player/monsters
        self.hp = max_hp
        self.max_hp = max_hp
        self.atk = atk
        self.dex = dex

        if group is not None:
            pg.sprite.Sprite.__init__(self, group)
        

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @x.setter
    def x(self, x):
        self.rect.x = x

    @y.setter
    def y(self, y):
        self.rect.y = y

    def update(self):
        self.draw()

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))

    # class to initilize a sprite with movement and actions

    def add_component(self, component):
        self.components[type(component)] = component

    def get(self, component):
        return self.components.get(component)

    def movement(self):  # def update(self)
        # updates sprite x and y coords

        dx = self.get(Velocity).dx * TILE_SIZE
        dy = self.get(Velocity).dy * TILE_SIZE
        self.rect.move_ip(dx, dy)


class Monster(Entity):

    def __init__(self, game, name, x, y, max_hp=10, atk=2, dex=2, item=None):
        super().__init__(game, x, y, game.monsters, name=name)

        self.in_combat = Flag(False)
        self.stun = 0
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.dex = dex
        self.item = item

    def ai(self):
        # enemy to player vector math here
        dx = 0
        dy = 0
        dx_player = self.game.player.get(Position).x - self.get(Position).x
        dy_player = self.game.player.get(Position).y - self.get(Position).y
        if math.sqrt(dx_player**2 + dy_player**2) < 5:
            if abs(dx_player) > abs(dy_player):
                if dx_player > 0:
                    dx = 1
                elif dx_player < 0:
                    dx = -1
            else:
                if dy_player > 0:
                    dy = 1
                elif dy_player < 0:
                    dy = -1
            self.get(Velocity).set(dx, dy)
        else:
            patrol_direction = randint(1, 4)
            dx = 0
            dy = 0

            if patrol_direction == 1:
                dx = 1
            elif patrol_direction == 2:
                dx = -1
            elif patrol_direction == 3:
                dy = 1
            elif patrol_direction == 4:
                dy = -1

            self.get(Velocity).set(dx, dy)


class Player(Entity):
    def __init__(self, name, game, x, y, filename=None):
        super().__init__(game, x, y, game.players, filename)
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
        if self.game.debug:
            print(f"Player at: {self.x},{self.y}")
        self.overworldcoords = [1, 1]  # overworld coordinates. starts at 1,1
        self.game.Movement.add_entity(self)
        self.game.Collision.add_entity(self)
        self.game.Combat.add_entity(self)


class Treasure(Entity):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, group=game.treasures, name="chest")
        self._layer = Layers.Door_Layer

        self.item = items[random.randint(1, 4)]


def create_monster(game, number):
    x = random.randint(1, X_TILES - 2)
    y = random.randint(1, Y_TILES - 2)
    if number == 0:
        return Monster(
            game,
            "Ogre",
            x,
            y,
            max_hp=20,
            atk=4,
            dex=0,
            item=items[random.randint(1, 4)],
        )
    elif number == 1:
        return Monster(
            game,
            "HobGoblin",
            x,
            y,
            max_hp=15,
            atk=2,
            dex=2,
            item=items[random.randint(1, 4)],
        )
    elif number == 2:
        return Monster(
            game,
            "Goblin",
            x,
            y,
            max_hp=10,
            atk=1,
            dex=2,
            item=items[random.randint(1, 4)],
        )
