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
                #if event.key == pygame.K_b:
                    #BattleMenu(self)  -Testing -Roland
                if event.key == pygame.K_w:
                    #Moves player incriments 
                    print(self.game.player.components.get(Position))
                    self.game.player.get(Velocity).set(0,-1)
                    self.game.movement.update_all()
                    print(self.game.player.components.get(Position))
                    self.game.player.movement()
                    #checks for player and wall overlap
                    #if true, moves player back 1
                    self.game.player.check_collisions(0, 1)
                    self.game.turn += 1 # don't increment if collision
                    self.game.draw()
                    self.game.monster.movement(self.game.player)
                    self.game.player.check_collisions(0, 1)
                    self.game.draw()
                if event.key == pygame.K_s:
                    
                    print(self.game.player.components.get(Position))
                    self.game.player.get(Velocity).set(0,1)
                    self.game.movement.update_all()
                    print(self.game.player.components.get(Position))
                    self.game.player.movement()
                    self.game.player.check_collisions(0, -1)
                    self.game.turn += 1
                    self.game.draw()
                    self.game.monster.movement(self.game.player)
                    self.game.player.check_collisions(0, -1)
                    self.game.draw()
                if event.key == pygame.K_a:
                    
                    print(self.game.player.components.get(Position))
                    self.game.player.get(Velocity).set(-1,0)
                    self.game.movement.update_all()
                    print(self.game.player.components.get(Position))
                    self.game.player.movement()
                    self.game.player.check_collisions(1, 0)
                    self.game.turn += 1
                    self.game.draw()
                    self.game.monster.movement(self.game.player)
                    self.game.player.check_collisions(1, 0)
                    self.game.draw()
                if event.key == pygame.K_d:
                    
                    self.game.player.check_collisions(-1, 0)
                    print(self.game.player.components.get(Position))
                    self.game.player.get(Velocity).set(1,0)
                    self.game.movement.update_all()
                    print(self.game.player.components.get(Position))
                    self.game.player.movement()
                    self.game.turn += 1
                    self.game.draw()
                    self.game.monster.movement(self.game.player)
                    self.game.player.check_collisions(-1, 0)
                    self.game.draw()
