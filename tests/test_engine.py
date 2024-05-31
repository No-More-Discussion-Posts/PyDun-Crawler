import pytest
import sys
from src.engine import Engine
import pygame 
import os
from src.config import *
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

@pytest.fixture
def game():
    game = Engine()
    game.new_game()
    game.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    return game

def test_move_up(game):
    
    player = game.player
    x = player.x
    y = player.y
    go_forward = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_w))
    game.handle_event(go_forward)
    new_x = player.x
    new_y = player.y
    assert new_y == (y-TILE_SIZE)

def test_move_down(game):
    player = game.player
    x = player.x
    y = player.y
    go_forward = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_s))
    game.handle_event(go_forward)
    new_x = player.x
    new_y = player.y
    assert new_y == (y+TILE_SIZE)