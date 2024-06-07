import pygame
from .ecs import System
from .components import Position,Velocity, TurnCounter
from ..entities import Player
from ..config import *
from .states import *

class Movement(System):
    
    def update(self):
        
        for entity in self.entities:
            entity.get(Position)+entity.get(Velocity)
            entity.movement()
            entity.get(Velocity).set(0,0)     
            if entity == self.entities[0]:
                self.entities[0].game.Turn.update()
            if entity.game.debug:
                print(f"{entity}: {entity.get(Position)}")

class Turn(System):

    def update(self):
        for entity in self.entities:
            entity.get(TurnCounter).turn += 1

    def undo(self):
        for entity in self.entities:
            entity.get(TurnCounter).turn -= 1
    
class Collision(System):

    def update(self):
        for entity in self.entities:
            #checks     player sprite(self) and and sprite in the blocks sprite group or overlap
            if pygame.sprite.spritecollide(entity, entity.game.blocks, False):
                if entity.game.debug:
                    print(f"{entity}: Collision with wall")
                #if there is overlap between player and wall sprites, the player the designated spot
                entity.get(Velocity).dx = entity.get(Velocity).p_dx * -1
                entity.get(Velocity).dy = entity.get(Velocity).p_dy * -1
                entity.game.Movement.update()
                #removes extra turn counter
                self.entities[0].game.Turn.undo()
                entity.movement()
            if isinstance(entity,Player): # should get rid of this eventually with better messaging/states/etc.
                if pygame.sprite.spritecollide(entity, entity.game.monsters, False):
                    
                        entity.game.state = GameStates.BATTLE
                
                elif pygame.sprite.spritecollide(entity, entity.game.doors, False):
                    #load map takes place before overworld check
                    #entity.game.load_map(NachoCheese)
                    
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
                    self.entities[0].game.Turn.undo()
                    entity.game.load_map(BLUE)

                
                elif pygame.sprite.spritecollide(entity, entity.game.treasures, True):
                    if entity.game.treasure.item != "Health Pot":
                        x = str(entity.game.treasure.item.keys())
                        #Don't Look I just wanted it to fucking work okay....don't judge me -Tyler
                        x = x.strip('dict_keys([\'\'])')
                        entity.equipped.equip_item(x,entity.game.treasure.item[x])
                    elif entity.game.treasure.item == "Health Pot":
                        entity.inventory.update_item(entity.game.treasure.item, 1)
                
