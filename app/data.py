"""API endpoints and object relational mapping"""
import db
import random
from db import GameEntity, Item, Inventory, InventoryItem
from db import Base, RoomWall, Tile, Room, Door, RoomDoor
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



test_dungeon = DungeonData()
# test_dungeon.new_dungeon()
test_dungeon.new_dungeon_with_size(8, 6)