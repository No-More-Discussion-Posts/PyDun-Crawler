import pytest
import pygame
from copd.ecs.components import Position,Velocity

def test_collide_wall(game):
    player = game.player
    monster = game.monster
    # Set Monster Position away from player
    monster.get(Position).x = 1
    monster.get(Position).y = 1

    # Set player position next to a wall
    # player.get(Position).x = 15
    # player.get(Position).y = 1

    # Move up into the wall
    for i in range(20):
        movement = pygame.event.Event(pygame.KEYDOWN,dict(key=pygame.K_w))
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    print(player.get(Position))
    assert (x,y) == (15,1)
    