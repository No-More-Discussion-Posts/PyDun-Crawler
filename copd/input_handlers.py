import pygame
from .menus import PauseMenu
from .ecs.states import GameStates
from .ecs.components import Velocity,Position


class EventHandler:
    def __init__(self,game):
        self.game = game

    def handle_event(self,event):
        if event.type == pygame.QUIT:
                self.game.running = False
        if self.game.state == GameStates.MAIN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PauseMenu(self.game)
                    self.game.draw()
                if event.key in [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d]:
                    self.game.player.get(Velocity).set_from_key(event.key)
                    self.game.Movement.update()
                    self.game.player.movement()
                    if self.game.monster.stun > 0:
                         self.game.monster.stun -= 1
                    else:
                        self.game.monster.movement()
                    self.game.Collision.update()
                    self.game.draw()