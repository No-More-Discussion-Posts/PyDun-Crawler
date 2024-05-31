import pytest
import sys
from copd.engine import Engine
import pygame 
import os
from copd.config import * 
from math import sqrt
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

def test_move_up(game):
    
    player = game.player
    x = player.x
    y = player.y
    movement = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_w))
    game.handle_event(movement)
    new_x = player.x
    new_y = player.y
    assert new_y == (y-TILE_SIZE)

def test_move_down(game):
    player = game.player
    x = player.x
    y = player.y
    movement = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_s))
    game.handle_event(movement)
    new_x = player.x
    new_y = player.y
    assert new_y == (y+TILE_SIZE)

def test_move_right(game):
    player = game.player
    x = player.x
    y = player.y
    movement = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_d))
    game.handle_event(movement)
    new_x = player.x
    new_y = player.y
    assert new_x == (x+TILE_SIZE)

def test_move_left(game):
    player = game.player
    x = player.x
    y = player.y
    movement = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_a))
    game.handle_event(movement)
    new_x = player.x
    new_y = player.y
    assert new_x == (x-TILE_SIZE)

def test_monster_movement(game):
    player = game.player
    monster = game.monster
    #ensure player is within range of monster
    monster.x = player.x + 2 * TILE_SIZE
    monster.y = player.y + 2 * TILE_SIZE
    monster.rect.x = monster.x
    monster.rect.y = monster.y

    distance = sqrt((player.x-monster.x)**2+(player.y-monster.y)**2)
    monster.movement(player)
    new_distance = sqrt((player.x-monster.x)**2+(player.y-monster.y)**2)

    assert new_distance < distance


    
