import pytest
from copd.engine import Engine
from copd.config import *
import pygame
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

@pytest.fixture(scope="session")
def game():
    game = Engine()
 
    game.load_start_map((0, 0, 255))

    # game.run()

    game.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    return game