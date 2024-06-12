import pygame
from copd.config import *
from math import sqrt
from copd.ecs.components import *
from .helpers import reset_player


# @reset_player()
def test_move_up(game):
    player = game.player
    print(f"{player}: {player.get(Position)}")

    y = player.get(Position).y
    # make player isn't against a wall
    if y == 1:
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_s))
        game.handle_event(movement)
    y = player.get(Position).y
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
    game.handle_event(movement)
    new_y = player.get(Position).y
    assert new_y == (y - 1)


def test_move_down(game):
    player = game.player
    y = player.get(Position).y
    # make player isn't against a wall
    if y == 15:
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
        game.handle_event(movement)
    y = player.get(Position).y
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_s))
    game.handle_event(movement)
    new_y = player.get(Position).y
    assert new_y == (y + 1)


def test_move_right(game):
    player = game.player
    x = player.get(Position).x
    y = player.get(Position).y
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_d))
    game.handle_event(movement)
    new_x = player.get(Position).x
    new_y = player.get(Position).y
    assert new_x == (x + 1)


def test_move_left(game):
    player = game.player
    x = player.get(Position).x
    y = player.get(Position).y
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_a))
    game.handle_event(movement)
    new_x = player.get(Position).x
    new_y = player.get(Position).y
    assert new_x == (x - 1)


def test_monster_movement(game):
    player = game.player
    monster = game.monster
    # ensure player is within range of monster
    monster.x = player.get(Position).x + 2 * TILE_SIZE
    monster.y = player.get(Position).y + 2 * TILE_SIZE
    monster.rect.x = monster.x
    monster.rect.y = monster.y

    distance = sqrt(
        (player.get(Position).x - monster.x) ** 2
        + (player.get(Position).y - monster.y) ** 2
    )
    monster.movement()
    new_distance = sqrt(
        (player.get(Position).x - monster.x) ** 2
        + (player.get(Position).y - monster.y) ** 2
    )

    assert new_distance <= distance
