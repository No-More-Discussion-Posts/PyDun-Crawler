import pytest 

def reset_player():
    def wrap(func):
        def wrapper(game):
            player = game.player
            game.Movement.remove_entity(player)
            game.Collision.remove_entity(player)
            game.add_player()
            player = game.player #should be brand new
            func(game)
        return wrapper
    return wrap