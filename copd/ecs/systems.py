import pygame
from .ecs import System
from .components import Position,Velocity
from ..entities import Player
from ..config import *
from .states import *

class Movement(System):
    
    def update(self):
        
        for entity in self.entities:
            entity.get(Position)+entity.get(Velocity)
            entity.movement()
            entity.get(Velocity).set(0,0)
            

class Collision(System):

    def update(self):
        for entity in self.entities:
            #checks     player sprite(self) and and sprite in the blocks sprite group or overlap
            if pygame.sprite.spritecollide(entity, entity.game.blocks, False):
                #if there is overlap between player and wall sprites, the player the designated spot
                entity.get(Velocity).dx = entity.get(Velocity).dx * -1
                entity.get(Velocity).dy = entity.get(Velocity).dy * -1
                # entity.get(Position)+entity.get(Velocity)
                entity.game.Movement.update()
                entity.movement()
            if isinstance(entity,Player): # should get rid of this eventually with better messaging/states/etc.
                if pygame.sprite.spritecollide(entity, entity.game.monsters, False):
                    
                        entity.game.state = GameStates.BATTLE
                
                elif pygame.sprite.spritecollide(entity, entity.game.doors, False):
                    entity.game.load_map(NachoCheese)
                    
                    if entity.get(Position).x == 0:
                        entity.get(Velocity).dx = 30
                        entity.overworldcoords[0] = entity.overworldcoords[0] - 1
                    elif entity.get(Position).x == 31:
                        entity.get(Velocity).dx = -30
                        entity.overworldcoords[0] = entity.overworldcoords[0] + 1
                    elif entity.get(Position).y == 0 :
                        entity.get(Velocity).dy = 16
                        entity.overworldcoords[1] = entity.overworldcoords[1] - 1
                    elif entity.get(Position).y == 17:
                        entity.get(Velocity).dy = -16
                        entity.overworldcoords[1] = entity.overworldcoords[1] + 1
                    entity.game.Movement.update()
                    entity.movement()
                
                # elif pygame.sprite.spritecollide(self, self.game.treasures, True):
                #     if self.game.treasure.item != "Health Pot":
                #         x = str(self.game.treasure.item.keys())
                #         #Don't Look I just wanted it to fucking work okay....don't judge me -Tyler
                #         x = x.strip('dict_keys([\'\'])')
                #         self.equipped.equip_item(x,self.game.treasure.item[x])
                #     elif self.game.treasure.item == "Health Pot":
                #         self.inventory.update_item(self.game.treasure.item, 1)
                
