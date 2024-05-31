"""Main Game Loop"""

# pause menu allow for inventory view
#  --- Save?

import pygame
from .engine import Engine


def main() -> None:
    """Main game loop"""
    game = Engine()
    game.new_game()
    game.run()


if __name__ == "__main__":
    main()
