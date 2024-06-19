"""Main Game Loop"""

# pause menu allow for inventory view
#  --- Save?

import pygame
import os
import sys

# Ensure copd can be imported even if not installed
if "copd" not in sys.modules:
    parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(parent_dir_name)
from copd.engine import Engine
from copd.config import *

pygame.init()


def main() -> None:
    """Main game loop"""
    game = Engine()
    game.add_player()
    game.load_map(DEFAULT_MAP)
    game.run()


if __name__ == "__main__":
    main()
