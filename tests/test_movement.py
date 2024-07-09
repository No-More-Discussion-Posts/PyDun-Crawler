import pygame
from copd.config import *
from math import sqrt
from copd.engine.components import *
from .helpers import reset_player


# @reset_player()
def test_move_up(game):
    player = game.player
    print(f"{player}: {player.get(Position)}")

    y = player.rect.y
    # make player isn't against a wall
    if y == 16:
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_s))
        game.handle_event(movement)
        for i in range(TILE_SIZE//ANIMATION_SPEED+1):
            player.update()
    # update after position change
    y = player.rect.y
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
    game.handle_event(movement)
    for i in range(TILE_SIZE//ANIMATION_SPEED+1):
        player.update()
    new_y = player.rect.y
    assert new_y == (y - TILE_SIZE)


# @reset_player()
def test_move_down(game):
    player = game.player

    y = player.rect.y
    # make player isn't against a wall
    if y == TILE_SIZE * (Y_TILES-1):
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_w))
        game.handle_event(movement)
        for i in range(TILE_SIZE//ANIMATION_SPEED+1):
            player.update()
    # update after position change
    y = player.rect.y
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_s))
    game.handle_event(movement)
    for i in range(TILE_SIZE//ANIMATION_SPEED+1):
        player.update()
    new_y = player.rect.y
    assert new_y == (y + TILE_SIZE)

def test_move_left(game):
    player = game.player

    x = player.rect.x
    # make player isn't against a wall
    if x == 16:
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_d))
        game.handle_event(movement)
        for i in range(TILE_SIZE//ANIMATION_SPEED+1):
            player.update()
    # update after position change
    x = player.rect.x
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_a))
    game.handle_event(movement)
    for i in range(TILE_SIZE//ANIMATION_SPEED+1):
        player.update()
    new_x = player.rect.x
    assert new_x == (x - TILE_SIZE)

def test_move_right(game):
    player = game.player

    x = player.rect.x
    # make player isn't against a wall
    if x == TILE_SIZE * (X_TILES-1):
        movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_a))
        game.handle_event(movement)
        for i in range(TILE_SIZE//ANIMATION_SPEED+1):
            player.update()
    # update after position change
    x = player.rect.x
    movement = pygame.event.Event(pygame.KEYDOWN, dict(key=pygame.K_d))
    game.handle_event(movement)
    for i in range(TILE_SIZE//ANIMATION_SPEED+1):
        player.update()
    new_x = player.rect.x
    assert new_x == (x + TILE_SIZE)

