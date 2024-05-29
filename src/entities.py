class Goblin:
    def __init__(self, lvl):
        #The lvl variable should be influenced by the global turn timer
        self.name = 'Goblin'
        self.max_hp = 10 * lvl
        self.hp = self.max_hp
        self.atk = 2 * lvl
        self.dex = 2.5 * lvl

class Hobgoblin:
    def __init__(self, lvl):
        self.name = 'HobGoblin'
        self.max_hp = 10 + (5 * lvl)
        self.hp = self.max_hp
        self.atk = 4 * lvl
        self.dex = 1 * lvl

class Ogre:
    def __init__(self, lvl):
        self.name = 'Ogre'
        self.max_hp = 20 + (5 * lvl)
        self.hp = self.max_hp
        self.atk = 6 * lvl
        self.dex = .5 * lvl

class Player:
    def __init__(self, name, lvl):
        self.name = name
        self.max_hp = 20
        self.hp = self.max_hp
        self.atk = 3 * lvl
        self.dex = 2 * lvl