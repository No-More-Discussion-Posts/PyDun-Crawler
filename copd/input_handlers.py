import pygame
from .menus import PauseMenu
from .states import GameStates
from .manager.components import Velocity,Position


class EventHandler:
    def __init__(self,game):
        self.game = game

    def handle_event(self,event):
        if self.game.state == GameStates.MAIN:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PauseMenu(self.game)
                    self.game.draw()
                if event.key in [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d]:
                    self.game.player.get(Velocity).set_from_key(event.key)
                    self.game.movement.update_all()
                    self.game.player.movement()
                    self.game.monster.movement()
                    self.game.movement.update_all()
                    self.game.player.check_collisions()
                    self.game.draw()