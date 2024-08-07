import pygame
from copd.ui.menus import PauseMenu
from copd.engine.states import GameStates
from copd.engine.components import Velocity, Position


class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):

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
                    self.game.Collision.update()
                    if self.game.debug:
                        print("Movement:")
                        print(f"{self.game.player}: {self.game.player.get(Position)}")
                    self.game.draw()
