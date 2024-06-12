import pytest
import pygame
import os
from copd.ecs.states import GameStates
from copd.menus import BattleMenu


def test_fight(game):
    game.state = GameStates.BATTLE
    player_hp = game.player.hp
    monster_hp = game.player.hp

    battle_menu = BattleMenu(game)
    battle_menu.combat(parry=False)

    assert player_hp > game.player.hp
    assert monster_hp > game.monster.hp


def test_parry(game):
    game.state = GameStates.BATTLE
    player_hp = game.player.hp
    monster_hp = game.player.hp

    battle_menu = BattleMenu(game)
    battle_menu.combat(parry=False)

    assert monster_hp > game.monster.hp
    # TODO: Add check for parry


# def test_run(game):
#     pass

# def test_player_death(game):
#     pass

# def test_monster_death(game):
#     pass
