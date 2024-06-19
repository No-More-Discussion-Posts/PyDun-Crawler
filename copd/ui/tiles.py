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

