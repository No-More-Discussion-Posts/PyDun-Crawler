import pygame
import sys
from random import randint
from copd.engine.ecs import System
from copd.engine.components import Position, Velocity, TurnCounter
from copd.engine.entities import Player, Monster
from copd.config import *
from copd.engine.states import *


class Movement(System):
    def update(self):
        """
        Updates x and y position of a
        moveable sprite based on the value
        of its velocity.
        """
        for entity in self.entities:
            if isinstance(entity, Monster):
                if entity.stun > 0:
                    entity.stun -= 1
                else:
                    entity.ai()

            dx = entity.get(Velocity).dx * TILE_SIZE
            dy = entity.get(Velocity).dy * TILE_SIZE

            if dx != 0 or dy != 0:
                entity.moving = True
                entity.x_dest = entity.rect.x + dx
                entity.y_dest = entity.rect.y + dy

                # Check for collision before moving
                if not self.check_collision(entity, dx, dy):
                    entity.rect.move_ip(dx, dy)  # Move entity by tile size
                    entity.prev_dx = dx
                    entity.prev_dy = dy
                else:
                    entity.moving = False

            entity.update()
            entity.get(Velocity).set(0, 0)

            if entity == self.entities[0]:
                self.entities[0].game.Turn.update()

    def check_collision(self, entity, dx, dy):
        future_rect = entity.rect.move(dx, dy)
        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = future_rect
        return pygame.sprite.spritecollideany(temp_sprite, entity.game.solid_blocks)


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
            if pygame.sprite.spritecollide(entity, entity.game.solid_blocks, False):
                if entity.game.debug:
                    print(f"{entity}: Collision with wall")
                entity.moving = False
                entity.rect.move_ip(-entity.prev_dx, -entity.prev_dy)
                entity.get(Velocity).set(0, 0)

                if isinstance(entity, Player):
                    entity.game.Turn.undo()
                    entity.game.monster.stun += 1

            if isinstance(entity, Player):
                door = pygame.sprite.spritecollide(entity, entity.game.doors, False)
                if len(door) > 0:
                    door = door[0]
                    entity.game.minimap.visit(entity.overworldcoords)
                    self.undo_movement(entity)
                    if door.rect.x == 0:
                        entity.get(Velocity).dx = X_TILES - 3
                        entity.overworldcoords[0] -= 1
                    elif door.rect.x == (X_TILES - 1) * TILE_SIZE:
                        entity.get(Velocity).dx = -(X_TILES - 3)
                        entity.overworldcoords[0] += 1
                    elif door.rect.y == 0:
                        entity.get(Velocity).dy = Y_TILES - 3
                        entity.overworldcoords[1] -= 1
                    elif door.rect.y == (Y_TILES - 1) * TILE_SIZE:
                        entity.get(Velocity).dy = -(Y_TILES - 3)
                        entity.overworldcoords[1] += 1
                    entity.game.Movement.update()
                    self.entities[0].game.Turn.undo()
                    entity.game.load_map()

                # If player overlaps with treasure, TRUE = delete treasure after collision
                elif pygame.sprite.spritecollide(entity, entity.game.treasures, False):
                    treasures = pygame.sprite.spritecollide(entity, entity.game.treasures, False)
                    for treasure in treasures:
                        if not treasure.collected:
                            treasure.collect()
                            room_id = entity.game.get_room_id()
                            room_state = entity.game.room_states.get(room_id, {'treasures': [], 'enemies': []})
                            for idx, (x, y, collected) in enumerate(room_state['treasures']):
                                if x == treasure.rect.x // TILE_SIZE and y == treasure.rect.y // TILE_SIZE:
                                    room_state['treasures'][idx] = (x, y, True)
                            entity.game.room_states[room_id] = room_state

                            # Add item to player's inventory
                            if treasure.item != "Health Pot":
                                item_type = list(treasure.item.keys())[0]
                                entity.equipped.equip_item(item_type, treasure.item[item_type])
                            elif treasure.item == "Health Pot":
                                entity.inventory.update_item(treasure.item, 1)


                monsters = pygame.sprite.spritecollide(entity, entity.game.monsters, False)
                if len(monsters) > 0:
                    monster = monsters[0]
                    self.undo_movement(entity)
                    self.undo_movement(monster)
                    monster.stun = 2  # Stun the monster for 2 turns
                    entity.game.state = GameStates.BATTLE

    def undo_movement(self, entity):
        entity.moving = False
        entity.rect.move_ip(-entity.prev_dx, -entity.prev_dy)
        entity.prev_dx = 0
        entity.prev_dy = 0
        entity.game.update()
class Combat(System):

    def __init__(self, game):
        super().__init__()
        self.complete = True
        self.game = game

    def end(self):
        try:
            self.game.player.in_combat.state = False
            self.game.monster.in_combat.state = False
            self.complete = True
        except Exception as e:
            print("Problem in Combat.end")
            print(e)

    def setup(self, parry=False):
        self.complete = False
        self.parry = parry
        self.game.player.in_combat.state = True
        self.game.monster.in_combat.state = True

    def update(self):
        try:
            self.player = self.entities[0].game.player
            self.monster = self.player.game.monster
            if self.player.in_combat.state and self.monster.in_combat.state:
                self.attack(self.player.game, parry=False)
        except Exception as e:
            print("Error in battle")
            print(e)

    def attack(self, game, parry):
        self.complete = False
        # Basic combat system can be improved later
        if game.debug:
            print("-----Battle Start-----")
            print(f"Player HP: {game.player.hp}")
            print(f"Monster HP: {game.monster.hp}")
        if parry:
            self.calc_parry(game)
        else:
            game.monster.hp -= game.player.atk
            game.player.hp -= game.monster.atk

        if game.debug:
            print("-----Battle Complete-----")
            print(f"Player HP: {game.player.hp}")
            print(f"Monster HP: {game.monster.hp}")

        if game.player.hp <= 0:
            pygame.quit()
            sys.exit()
        elif game.monster.hp <= 0:
            self.handle_monster_defeat(game)
            self.complete = True

    def handle_monster_defeat(self, game):
        """Handle logic for when a monster is defeated."""
        try:
            if game.monster.item != "Health Pot":
                item_type = list(game.monster.item.keys())[0]
                game.player.equipped.equip_item(item_type, game.monster.item[item_type])
            elif game.monster.item == "Health Pot":
                game.player.inventory.update_item(game.monster.item, 1)

            # Update room state
            room_id = game.get_room_id()
            room_state = game.room_states.get(room_id, {'treasures': [], 'enemies': []})
            enemy_type = game.monster.type  # Ensure your monster has a number attribute for type

            # Remove the monster from the room state
            for idx, (type, x, y, alive) in enumerate(room_state['enemies']):
                if x == game.monster.rect.x // TILE_SIZE and y == game.monster.rect.y // TILE_SIZE:
                    room_state['enemies'][idx] = (type, x, y, False)
            game.room_states[room_id] = room_state

            game.monster.die()

        except ValueError as e:
            print(f"Error in removing monster: {e}")

    def calc_parry(self, game) -> bool:
        """Parry attack: Chance to deal extra damage and take no damage.

        Returns
        -------
        bool
            True - Successfully parried
            False - Failed to parry
        """
        # Parry Chance is calculated by miss_hit function in entities
        parry_chance = self.miss_hit(game.player.dex)
        if parry_chance:
            game.monster.hp -= (game.player.atk + game.monster.atk)
        else:
            game.monster.hp -= game.player.atk
            game.player.hp -= game.monster.atk
        return parry_chance

    ###TYLER EXPERIMENTAL###
    def miss_hit(self, player_dex):
        pdex = player_dex
        chance_hit = randint(1, 10)
        if chance_hit <= pdex:
            return True
        return False