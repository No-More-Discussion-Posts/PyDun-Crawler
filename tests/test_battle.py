import pytest
import pygame
import os
from copd.ecs.states import GameStates
from copd.menus import BattleMenu
from .helpers import reset_player, reset_monster


@reset_player()
@reset_monster()
def test_fight(game):
    game.state = GameStates.BATTLE
    player_hp = game.player.hp
    monster_hp = game.monster.hp

    battle_menu = BattleMenu(game)
    battle_menu.combat(parry=False)

    assert game.player.hp == player_hp - game.monster.atk
    assert game.monster.hp == monster_hp - game.player.atk


def test_parry(game):
    game.state = GameStates.BATTLE
    player_hp = game.player.hp
    monster_hp = game.player.hp

    battle_menu = BattleMenu(game)
    parried = False
    for i in range(100):
        parried = battle_menu.parry()
        if parried:
            break
        elif game.player.hp <= 0:
            game.player.hp = game.player.max_hp
        elif game.monster.hp <= 0:
            game.monster.hp = game.monster.max_hp
    assert parried == True

    assert monster_hp > game.monster.hp
    # TODO: Add check for parry


# def test_run(game):
#     pass

# def test_player_death(game):
#     pass

# def test_monster_death(game):
#     pass
