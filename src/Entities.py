import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y) -> None:
        self.game = game
        self.image = pg.surface(())
        self.image.fill((255,255, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def movement(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * 20
        self.rect.y = self.y * 20

class Monster(pg.sprite.Sprite):
    def __init__(self, game, x, y) -> None:
        pass

    def move():
        pass
        
class Wall():
    def __init__(self, game, x, y) -> None:
        pass

    def move():
        pass

class Door():
    def __init__(self, game, x, y) -> None:
        pass

class Treasure():
    def __init__(self, game, x, y) -> None:
        pass