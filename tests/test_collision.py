import pytest
import pygame
from copd.engine.components import Position, Velocity
from copd.engine.engine import Engine
from copd.config import *
from .helpers import *


@reset_player()
@no_monster()
def test_collide_wall_n(game: Engine):
    player = game.player
    (test_x,test_y),dist = get_collision_position(player,'n')
    # Move up into the wall
    player.moving = True
    # Move to one block away
    player.x_dest = test_x
    player.y_dest = test_y+TILE_SIZE
    while player.rect.y != test_y+TILE_SIZE:
        # Need to update multiple times due to animation
        player.update()
    # Try to move into solid block
    player.y_dest = test_y
    player.update()
    # Check for collision
    game.Collision.update()

    x = player.rect.x
    y = player.rect.y
    assert (x, y) == (test_x, test_y+TILE_SIZE)

@reset_player()
@no_monster()
def test_collide_wall_w(game: Engine):
    player = game.player
    (test_x,test_y),dist = get_collision_position(player,'w')
    # Move up into the wall
    player.moving = True
    # Move to one block away
    player.x_dest = test_x+TILE_SIZE
    player.y_dest = test_y
    while player.rect.x != test_x+TILE_SIZE:
        # Need to update multiple times due to animation    
        player.update()
    # Try to move into solid block
    player.x_dest = test_x
    player.update()
    # Check for collision
    game.Collision.update()

    x = player.rect.x
    y = player.rect.y
    assert (x, y) == (test_x+TILE_SIZE, test_y)


@reset_player()
@no_monster()
def test_collide_wall_s(game: Engine):
    player = game.player
    (test_x,test_y),dist = get_collision_position(player,'s')
    # Move up into the wall
    player.moving = True
    # Move to one block away
    player.x_dest = test_x
    player.y_dest = test_y-TILE_SIZE
    while player.rect.y != test_y-TILE_SIZE:
        # Need to update multiple times due to animation
        player.update()
    # player.update()
    # Try to move into solid block
    player.y_dest = test_y
    player.update()
    # Check for collision
    game.Collision.update()

    x = player.rect.x
    y = player.rect.y
    assert (x, y) == (test_x, test_y-TILE_SIZE)


@reset_player()
@no_monster()
def test_collide_wall_e(game: Engine):
    player = game.player
    (test_x,test_y),dist = get_collision_position(player,'e')
    # Move up into the wall
    player.moving = True
    # Move to one block away
    player.x_dest = test_x-TILE_SIZE
    player.y_dest = test_y
    while player.rect.x != test_x-TILE_SIZE:
        # Need to update multiple times due to animation
        player.update()
    # player.update()
    # Try to move into solid block
    player.x_dest = test_x
    player.update()
    # Check for collision
    game.Collision.update()

    x = player.rect.x
    y = player.rect.y
    assert (x, y) == (test_x-TILE_SIZE, test_y) 
