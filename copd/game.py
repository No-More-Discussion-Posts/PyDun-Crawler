"""Main Game Loop"""

# pause menu allow for inventory view
#  --- Save?

import pygame
import os
import sys
if 'copd' not in sys.modules:
    parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(parent_dir_name)
from copd.engine import Engine


def main() -> None:
    """Main game loop"""
    game = Engine()
    game.new_game()
    game.run()


if __name__ == "__main__":
    main()