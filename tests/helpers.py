import pytest
from copd.config import *
from copd.engine.components import *

def get_collision_position(player,direction):
    game = player.game
    player_x,player_y = player.rect.x,player.rect.y
    x,y = 0,0
    test_x,test_y = 0,0
    # Get wall in line with player
    sprite = None
    dist = 0
    
    for block in game.solid_blocks.sprites():
        test_x = block.rect.x
        test_y = block.rect.y

        if direction == "n":
            # block y should be less than player y
            if player_x == test_x and player_y > test_y:
                # inline vertically with block
                new_dist = player_y - test_y
                
                if dist > new_dist or dist == 0:
                    dist = new_dist 
                    x = test_x
                    y = test_y - TILE_SIZE
                
               
        elif direction == "s":
            if player_x == test_x and player_y < test_y:
                new_dist = test_y - player_y
                if dist > new_dist or dist == 0:
                    dist = new_dist
                    x = test_x
                    y = test_y

        elif direction == "e":
            if player_y == test_y and player_x < test_x:
                new_dist = test_x - player_x
                if dist > new_dist or dist == 0:
                    dist = new_dist
                    x = test_x
                    y = test_y

        elif direction == "w":
            if player_y == test_y and player_x > test_x:
                new_dist = player_x - test_x
                if dist > new_dist or dist == 0:
                    dist = new_dist
                    x = test_x
                    y = test_y

    return (x,y),dist
def reset_player():
    def wrap(func):
        def wrapper(game):
            player = game.player
            game.Movement.remove_entity(player)
            game.Collision.remove_entity(player)
            game.add_player()
            player = game.player  # should be brand new
            func(game)

        return wrapper

    return wrap


def reset_monster():
    def wrap(func):
        def wrapper(game):
            game.monster.kill()
            game.monster = None
            game.add_monster(game.get_room_id())  # should be brand new
            func(game)

        return wrapper

    return wrap


def no_monster():
    def wrap(func):
        def wrapper(game):
            game.Movement.remove_entity(game.monster)
            game.Collision.remove_entity(game.monster)
            game.monster.kill()
            # del game.monster
            func(game)

        return wrapper

    return wrap
