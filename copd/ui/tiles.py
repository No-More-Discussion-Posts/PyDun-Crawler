import csv
import os
import pygame
import yaml
from yaml import CLoader
from pathlib import Path
from copd.engine.entities import Entity
from copd.config import *

class TileMap:
    def __init__(self,filename:Path):
        self.tile_map = pygame.image.load(filename)
        data_file = Path(str(filename).replace('png','yaml'))
        self.data = yaml.load(data_file.read_text(),CLoader)

    def get_image(self,name:str):
        if name in self.data:
            data = self.data[name]
            sprite = pygame.Surface((TILE_SIZE,TILE_SIZE))
            sprite.set_colorkey((0,0,0))
            sprite.blit(self.tile_map,(0,0),(data['x'],data['y'],TILE_SIZE,TILE_SIZE))
            return sprite
        else:
            raise KeyError(f"No sprite found with the name: {name}")
class Map:
    def __init__(self,game,filename):
        self.game = game
        self.start_x = 0
        self.start_y = 0
        self.filename = filename

    def read_csv(self):
        map = []
        with open(os.path.join(self.filename)) as data:
            data = csv.reader(data,delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self):
        map = self.read_csv()
        x,y = 0,0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    group=self.game.solid_blocks
                    name = "wall"
                elif tile == '1':
                    group = self.game.blocks
                    name = "floor"
                elif tile == '2':
                    group = self.game.doors
                    name = "door"

                Entity(self.game,x, y,group=group,name=name).draw()
                x+=1
            y += 1
