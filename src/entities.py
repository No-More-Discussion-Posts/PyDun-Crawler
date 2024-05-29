import random
from inventory import Inventory

class Goblin:
    def __init__(self, lvl):
        #The lvl variable should be influenced by the global turn timer
        self.name = 'Goblin'
        self.max_hp = 10 + (2 * lvl)
        self.hp = 10 + (2 * lvl)
        self.atk = 2 * lvl
        #self.dex = 2.5 * lvl

class Hobgoblin:
    def __init__(self, lvl):
        self.name = 'HobGoblin'
        self.max_hp = 10 + (5 * lvl)
        self.hp = 10 + (5 * lvl)
        self.atk = 4 * lvl
        #self.dex = 1 * lvl

class Ogre:
    def __init__(self, lvl):
        self.name = 'Ogre'
        self.max_hp = 20 + (5 * lvl)
        self.hp = 20 + (5 * lvl)
        self.atk = 6 * lvl
        #self.dex = .5 * lvl

class Player:
    def __init__(self, name, lvl):
        self.name = name
        self.max_hp = 20
        self.hp = 20
        self.atk = 3 * lvl
        #self.dex = 2 * lvl
        self.inventory = Inventory()


def miss_hit(player_dex, enemy_dex):
    pdex = player_dex
    edex = enemy_dex
    if edex > pdex:
        miss_chance = int(100-((pdex/edex)*100))
    elif pdex > edex:
        miss_chance = 0
    if miss_chance == 0:
        return True
    elif miss_chance >= 100:
        return False
    elif 100 > miss_chance > 0:
        y = random.randint(1, 100)
        if y > miss_chance:
            return True
        elif y < miss_chance:
            return False