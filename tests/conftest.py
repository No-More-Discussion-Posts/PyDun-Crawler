import pytest
import pygame
import os
import sys
from importlib import reload

if "copd" not in sys.modules:
    parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(parent_dir_name)

from copd.engine.engine import Engine
from copd.config import *

os.environ["SDL_VIDEODRIVER"] = "dummy"


@pytest.fixture(scope="function")
def game():

    pygame.init()
    mygame = Engine()
    mygame.add_player()
    mygame.load_map()

    # game.run()

    mygame.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    return mygame
