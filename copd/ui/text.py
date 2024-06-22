import pygame
from pathlib import Path
import yaml
from yaml import CLoader
from copd.config import *

def render_text(text, size=16):
    tile_map = pygame.image.load(Path("copd/ui/assets/tilemap.png"))
    data_file = Path("copd/ui/assets/tilemap.png".replace("png", "yaml"))
    data = yaml.load(data_file.read_text(), CLoader)
    surface = pygame.Surface((TILE_SIZE * len(text), TILE_SIZE))
    surface.set_colorkey((0, 0, 0))
    for i,char in enumerate(text):
        c_data = data[char]
        surface.blit(tile_map, (i*TILE_SIZE, 0), (c_data["x"], c_data["y"], TILE_SIZE,TILE_SIZE))
    if size != TILE_SIZE:
        surface = pygame.transform.scale(surface, (len(text)*size, size))
    return surface