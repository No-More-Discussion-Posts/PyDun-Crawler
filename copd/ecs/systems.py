import pygame
from .ecs import System
from .components import Position,Velocity
from ..entities import Player
from .states import *

class Movement(System):
    
    def update(self):
        for entity in self.entities:
            entity.get(Position)+entity.get(Velocity)
            

class Collision(System):

    def update(self):
        for entity in self.entities:
            #checks     player sprite(self) and and sprite in the blocks sprite group or overlap
            if pygame.sprite.spritecollide(entity, entity.game.blocks, False):
                #if there is overlap between player and wall sprites, the player the designated spot
                entity.get(Velocity).dx = entity.get(Velocity).dx * -1
                entity.get(Velocity).dy = entity.get(Velocity).dy * -1
                entity.get(Position)+entity.get(Velocity)
                entity.movement()
            
            elif pygame.sprite.spritecollide(entity, entity.game.monsters, False):
                if isinstance(entity,Player):
                    entity.game.state = GameStates.BATTLE
            
            elif pygame.sprite.spritecollide(entity, entity.game.doors, False):
                # self.game.load_map(FAFO_MAP)
                print("Door")

