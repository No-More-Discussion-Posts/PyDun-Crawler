import pytest
import pygame
import os
import sys
if 'copd' not in sys.modules:
    parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(parent_dir_name)
from copd.engine import Engine
from copd.config import *

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

@pytest.fixture(scope="session")
def game():
    game = Engine()
 
    game.load_start_map((0, 0, 255))

    # game.run()

    game.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    return game