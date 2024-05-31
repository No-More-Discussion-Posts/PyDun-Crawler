import pytest
from src.engine import Engine
from src.config import *
import pygame 

@pytest.fixture
def game():
    game = Engine()
    game.new_game()
    game.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    return game