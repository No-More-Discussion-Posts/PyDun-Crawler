import pygame
from ..ui.menus import PauseMenu
from .states import GameStates
from .components import Velocity, Position


class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        if self.game.debug:
            print(f"New Event: {event}")
            print(f"Game State: {self.game.state}")
        if event.type == pygame.QUIT:
            self.game.running = False
        if self.game.state == GameStates.MAIN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PauseMenu(self.game)
                    self.game.draw()
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    self.game.player.get(Velocity).set_from_key(event.key)
                    self.game.Movement.update()
                    self.game.player.movement()
                    if self.game.monster.stun > 0:
                        self.game.monster.stun -= 1
                    else:
                        self.game.monster.movement()
                    self.game.Collision.update()
                    if self.game.debug:
                        print("Movement:")
                        print(f"{self.game.player}: {self.game.player.get(Position)}")
                    self.game.draw()
