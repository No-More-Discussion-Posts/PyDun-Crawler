import pygame
from .ecs import System
from .components import Position,Velocity, TurnCounter
from ..entities import Player
from ..config import *
from .states import *

class Movement(System):
    
    def update(self):
        """
        updates x and y position of a
        moveable sprite based on the value
        of its velocity
        """
        #loops through all all entitites added by
        #system
        for entity in self.entities:
            #get x, y of sprite, adds changes
            entity.get(Position)+entity.get(Velocity)
            #updates sprite position
            entity.movement()
            #resets velocity
            entity.get(Velocity).set(0,0)     
            if entity == self.entities[0]:
                #update turn timer after movement
                self.entities[0].game.Turn.update()
            if entity.game.debug:
                #debbuger
                print(f"{entity}: {entity.get(Position)}")

class Turn(System):

    def update(self):
        for entity in self.entities:
            entity.get(TurnCounter).turn += 1

    def undo(self):
        for entity in self.entities:
            entity.get(TurnCounter).turn -= 1
    
class Collision(System):
    """
    This class checks any sprite on sprite collisions
    and then performs an action depeding on sprites colliding.
    sprites "collide" on overlap, not adjacenty
    """
    def update(self):
        for entity in self.entities:
            #checks all entities in system for collision with sprites
            #in the wall group of sprites
            if pygame.sprite.spritecollide(entity, entity.game.blocks, False):
                if entity.game.debug:
                    print(f"{entity}: Collision with wall")
                #return sprite to original position
                entity.get(Velocity).dx = entity.get(Velocity).p_dx * -1
                entity.get(Velocity).dy = entity.get(Velocity).p_dy * -1
                entity.game.Movement.update()
                #remove turn counter after returning sprite
                self.entities[0].game.Turn.undo()
                entity.movement()
            
            ###PLAYER SPECIFIC COLLISION###
            if isinstance(entity,Player):
                #if overlap with monster sprite, begin combat gamestate
                if pygame.sprite.spritecollide(entity, entity.game.monsters, False):
                        entity.game.state = GameStates.BATTLE
                #if overlap with door sprite group, load new area
                elif pygame.sprite.spritecollide(entity, entity.game.doors, False):
                    #loads sprite on corresponding doors
                    if entity.get(Position).x == 0:
                        entity.get(Velocity).dx = 30
                        #updates minimap
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
                    #pushes new x and y coords to sprite
                    entity.game.Movement.update()
                    entity.movement()
                    #resets turn timer
                    self.entities[0].game.Turn.undo()
                    #calls load map to draw new room
                    entity.game.load_map(BLUE)

                #if player overlaps with treasure, TRUE = delete treasure after collsion
                elif pygame.sprite.spritecollide(entity, entity.game.treasures, True):
                    #checks if item in chest is health pot
                    if entity.game.treasure.item != "Health Pot":
                        #adds equipment assigned to treasure object
                        # to players inventory
                        x = str(entity.game.treasure.item.keys())
                        x = x.strip('dict_keys([\'\'])')
                        entity.equipped.equip_item(x,entity.game.treasure.item[x])
                    elif entity.game.treasure.item == "Health Pot":
                        #adds health pot to player inventory
                        entity.inventory.update_item(entity.game.treasure.item, 1)
                
