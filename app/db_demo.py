"""
    Simple PyGame window for drawing db visualizations.

"""

import pygame
import os
import sys
from api import DungeonDB

if "copd" not in sys.modules:
    parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(f"Adding: {parent_dir_name}")
    sys.path.append(parent_dir_name)
from copd.engine import Engine
from copd.ui.tiles import Map

MAP_X = 40
MAP_Y = 20


def create_demo_map(x, y):
    map = [[*range(x)], [*range(y)]]
    print(map)
    return map


def main() -> None:
    """Main game loop"""
    """
    game = Engine()
    #game.load_start_map((0, 0, 255), map=DEFAULT_MAP)

    map = create_demo_map(MAP_X, MAP_Y)
    #game.load_start_map(color=(0, 0, 255))

    map = Map(game=game, filename='./app/demomap.csv')
    game.load_start_map(color=(0, 0, 255), map=map)

    game.Test_Grid()
    """

    # game.run()
    db = DungeonDB()
    map = db.generate_new_level()
    print(map)


class demo_engine:
    # TODO hook this into the ecs and create a simple map engine
    pass

    if __name__ == "__main__":
        main()
