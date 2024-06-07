import pytest
import pygame
from copd.ecs.components import Position,Velocity
from .helpers import *

def test_collide_wall_n(game):
    player = game.player
    monster = game.monster
    # Set Monster Position away from player
    monster.get(Position).x = 1
    monster.get(Position).y = 1

    # Move up into the wall
    for i in range(20):
        movement = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_w))
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    print(player.get(Position))
    assert (x,y) == (15,1)
    


@reset_player()
def test_collide_wall_s(game):
    player = game.player #should be brand new

    for i in range(20):
        movement = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_s))
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    print(player.get(Position))
    assert (x,y) == (15,16)