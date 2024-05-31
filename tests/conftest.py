import pytest
from copd.engine import Engine
from copd.config import *
import pygame


@pytest.fixture
def game():
    game = Engine()
    game.new_game()
    game.load_map()
    game.add_player()
    game.add_monster()
    game.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    return game