import pytest


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
            game.add_monster()  # should be brand new
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
