import pytest
import sys
from src.engine import Engine
import pygame 

def test_movement():
    game = Engine()
    game.new_game()
    # game.running = True # force it to think the game is running
    player = game.player
    x = player.x
    y = player.y
    go_forward = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_w))
    game.handle_event(go_forward)
    new_x = player.x
    new_y = player.y
    assert (x,y) != (new_x,new_y)