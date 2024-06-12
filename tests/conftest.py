import pytest
import pygame
import os
import sys

if "copd" not in sys.modules:
    parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(parent_dir_name)


os.environ["SDL_VIDEODRIVER"] = "dummy"


@pytest.fixture(scope='function')
def game():
    from copd.engine import Engine
    from copd.config import SCREEN_HEIGHT, SCREEN_WIDTH

    pygame.init()
    mygame = Engine()

    mygame.load_start_map((0, 0, 255))

    # game.run()

    mygame.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    yield mygame
