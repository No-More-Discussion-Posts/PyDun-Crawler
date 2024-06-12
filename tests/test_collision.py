import pytest
import pygame
from copd.ecs.components import Position, Velocity
from copd.engine import Engine
from .helpers import *


@no_monster()
def test_collide_wall_n(game: Engine):
    player = game.player

    # Move up into the wall
    for i in range(20):
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    print(player.get(Position))
    assert (x, y) == (15, 1)


@no_monster()
def test_collide_wall_s(game: Engine):
    player = game.player  # should be brand new

    for i in range(20):
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_s))
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    print(player.get(Position))
    assert (x, y) == (15, 16)


def test_collide_wall_e(game):
    player = game.player  # should be brand new
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
    game.handle_event(movement)
    for i in range(20):
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_d))
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    print(player.get(Position))
    assert (x, y) == (30, 8)

@reset_player()
def test_collide_wall_w(game):
    player = game.player  # should be brand new
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
    game.handle_event(movement)

    for i in range(20):
        print(f"Move {i}")
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_a))
        game.handle_event(movement)
    x = player.get(Position).x
    y = player.get(Position).y
    assert (x, y) == (1, 8)
