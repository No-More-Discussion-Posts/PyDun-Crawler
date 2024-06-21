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

    # Move up into the wall
    for i in range(20):
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
        game.handle_event(movement)
        player.update()
    x = player.x
    y = player.y
    print(player.get(Position))
    assert (x, y) == (15*TILE_SIZE, 1*TILE_SIZE)


@reset_player()
@no_monster()
def test_collide_wall_s(game: Engine):
    player = game.player  # should be brand new

    for i in range(20):
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_s))
        game.handle_event(movement)
        player.update()
    player.update()
    x = player.x
    y = player.y
    print(player.get(Position))
    assert (x, y) == (15*TILE_SIZE, (Y_TILES - 2)*TILE_SIZE)


@reset_player()
@no_monster()
def test_collide_wall_e(game):
    player = game.player  # should be brand new
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
    game.handle_event(movement)
    for i in range(30):
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_d))
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    print(player.get(Position))
    assert (x, y) == (X_TILES - 2, 8)


@reset_player()
@no_monster()
def test_collide_wall_w(game):
    player = game.player  # should be brand new
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
    pygame.event.post(movement)
    game.handle_event(movement)

    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_a))
    for i in range(20):
        print(f"Move {i}")
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    assert (x, y) == (1, 8)
