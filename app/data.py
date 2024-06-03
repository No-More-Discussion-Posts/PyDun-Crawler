"""API endpoints and object relational mapping"""
import db
import random
from db import GameEntity, Item, Inventory, InventoryItem
from db import Base, RoomWall, DungeonTile, Room, Door, RoomDoor
from sqlalchemy import select
from sqlalchemy.orm import Session


class Data():
    
    def get_array():
        pass

class DungeonData(Data):
    # TODO: build out methods for breaking out new maps
    def new_dungeon(self): # TODO: refactor this to __init__?
        self.create_room_walls()

    def new_dungeon_with_size(self, x, y): # TODO: take x and y values for grid
        self.create_room_walls()
        # create seed room
        seed_x = random.randint(0, x)
        seed_y = random.randint(0, y)
        self.create_room(0, seed_x, seed_y)
        self.read_room_walls()
        walls = self.read_room_walls()
        print("room walls: ")

        # decide which walls get a door
            # no = door (with null room)
            # maybe = null
            # yes = door (with room)
        
        # if adding a door, check existence of opposite room

        # if room already exists, check if door can be created
            # if door null door exists on other side
            # if door does not exist on other side, add both new doors


    def new_seed_room(self, x, y):
        pass

    # TODO: Write CRUD methods for each table
    # Create
    def create_game_entity(self, id, name):
        with Session(db.engine) as session:
            game_entity = GameEntity(id = id, name = name)
        session.add(game_entity)
        session.commit()

    def create_item(self, id, name):
        with Session(db.engine) as session:
            item = Item(id = id, name = name)
        session.add(item)
        session.commit()

    def create_inventory(self, id, entity_id):
        with Session(db.engine) as session:
            inventory = Inventory(id = id, entity_id = entity_id)
        session.add(inventory)
        session.commit()

    def create_inventory_item(self, inventory_id, item_id):
        with Session(db.engine) as session:
            inventory_item = InventoryItem(id = id, inventory_id = inventory_id, item_id = item_id)
        session.add(inventory_item)
        session.commit()

    def create_room_walls(self):
        """Hardcoded room_wall values"""
        with Session(db.engine) as session:
            north = RoomWall(id = 0, side = "north", pair = 2)
            east = RoomWall(id = 1, side = "east", pair = 3)
            south = RoomWall(id = 2, side = "south", pair = 0)
            west = RoomWall(id = 3, side = "west", pair = 1)
        session.add_all([north, east, south, west])
        session.commit()

    def create_dungeon_tile(self, id, room_id):
        """Insert new dungeon with arguments"""
        with Session(db.engine) as session:
            tile = DungeonTile(id = id, room_id = room_id)
        session.add(tile)
        session.commit()

    def create_room(self, id, x, y):
        with Session(db.engine) as session:
            room = Room(id = id, x = x, y = y)
        session.add(room)
        session.commit()

    def create_door(self, id, room_id):
        with Session(db.engine) as session:
            door = Door(id=id, room_id = room_id)
        session.add(door)
        session.commit()

    def create_room_door(self, id, room_wall_id, door_id):
        with Session(db.engine) as session:
            room_door = RoomDoor(id=id, room_id = room_wall_id, door_id = door_id)
        session.add(room_door)
        session.commit()


    # Read
    def read_game_entity(self):
        pass
    def read_item(self):
        pass
    def read_inventory(self):
        pass
    def read_inventory_item(self):
        pass
    def read_room_walls(self):
        walls = []
        with Session(db.engine) as session:
            stmt = select(RoomWall).distinct()
        return session.execute(stmt)
    def read_dungeon(self):
        pass
    def read_room(self):
        pass
    def read_door(self):
        pass
    def read_room_door(self):
        pass

    # Update
    def update_game_entity(self):
        pass
    def update_item(self):
        pass
    def update_inventory(self):
        pass
    def update_inventory_item(self):
        pass
    def update_room_walls():
        pass
    def update_dungeon():
        pass
    def update_room():
        pass
    def update_door():
        pass
    def update_room_door():
        pass

    # Delete
    def delete_game_entity(self):
        pass
    def delete_item(self):
        pass
    def delete_inventory(self):
        pass
    def delete_inventory_item(self):
        pass
    def delete_room_walls():
        pass
    def delete_dungeon():
        pass
    def delete_room():
        pass
    def delete_door():
        pass
    def delete_room_door():
        pass


test_dungeon = DungeonData()
# test_dungeon.new_dungeon()
test_dungeon.new_dungeon_with_size(8, 6)