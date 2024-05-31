from enum import Enum

class GameStates(Enum):
	MAIN = 1              # Player in the map walking around
	BATTLE = 2            # In the Battle Menu
	PAUSED = 3            # Game Paused
	INVENTORY = 4         # In the Inventory Menu