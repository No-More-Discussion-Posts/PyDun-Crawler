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
    game.new_game()
    game.load_map()
    game.add_player()
    game.add_monster()
    game.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    return game