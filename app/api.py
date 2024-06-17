"""
    Internal API with endpoints for game data.
"""

import random
from db import DB
from db import Room
from sqlalchemy import *
from sqlalchemy.orm import *

MAP_X = 40
MAP_Y = 20
ROOM_LIMIT = 10

engine = create_engine("sqlite://", echo=True)
database = DB()

class API:
    def __init__(self, engine=None, db=None) -> None:
        if engine is not None:
            self.engine = engine
        if db is not None:
            self.database = db

class PlayerDB(API):
    def __init__(self, engine=None, db=None) -> None:
        super().__init__(engine, db)
        pass


class DungeonDB(API):
    def __init__(self, engine=None, db=None) -> None:
        super().__init__(engine, db)
        self.database = DB()
        self.database.create_walls()


# TODO: create dungeon map generator

# this needs to return a 2d array of room_ids
# each room_id must correspond to a unique room object

# basic dun gen sequence:
    
    def generate_new_level(self, x=None, y=None) -> None:
    
        # define map boundaries (can be hard-coded maybe)
        if x is None:
            x = MAP_X
        if y is None:
            y = MAP_Y

        # create 2d array
        map_coords = [[*range(x)],[*range(y)]]
        #print(map_coords)
        map_array = [[0 for col in map_coords[1]] for row in map_coords[0]]
        
        # pick a random seed room (this will be "room 0")
        seed_x = random.choice(map_coords[0])
        seed_y = random.choice(map_coords[1])
        map_array[seed_x][seed_y] = 1        

        #print(map_array)
        print (f"seed room = {seed_x},{seed_y}")
        
        # call room gen method

        # pick a random to declare as exit

        
    # room gen sequence
    def generate_room(self, x, y, first_wall=None, room_id=None):
        
        # create new room
        if room_id is None:
            room_id = 1
        
        # This is mostly to help prevent 1 vs 0 based indexing issues...
        test_room_id = self.database.create_room(0, 0, 0)
        room_id = self.database.create_room(id=room_id, x=x, y=y)
        
        # Testing 
        first_room = self.database.read_room()
        all_rooms = self.database.read_rooms()
        print("rooms: ")
        for room in all_rooms:
            print(room)
        print(f"first room: {first_room}")

        # No first wall implies seed room,
        # assign random first wall
        if first_wall is None:
            first_wall = random.randint(0,3)
        print(first_wall)
        
        # randomise wall choice
        walls = list(range(4))
        random.shuffle(walls)
        walls.insert(0, walls.pop(walls.index(first_wall)))
        print(f"walls = {walls}")
                
        # create a new set of room_wall_doors
        for wall in walls:
            # randomly decide which walls get a door
            if walls.index(wall) == 0:
                door_choice = 1
            else:
                door_choice = random.randint(-1,1)

            # choose between no, maybe, or yes
            # no = null room (door with null room_id)
            # maybe = null
            # yes = door (with not room)

            door_id = None # maybe door
            if door_choice != 0:
                # create new door with room.id = null
                door_id = self.database.create_door()
            # this.door_id = new_door.id
            rwd_id = self.database.create_room_wall_door(room_id=room_id, wall_id=wall, door_id=door_id)
            #door_id = self.database.create_door(room_id=room_id) # door.
            print(rwd_id)
            # if "no door", don't update door
            # if "yes door"  

            wall_pair = self.database.get_opposite_wall(wall)
            print(f"wall = {wall}, pair = {wall_pair}")
            
            that_room_id = 0 # invalid room (should start at 1)
            
            # door_choice == 1 # For testing
            if door_choice == 1:
                #pass
                
            # check if opposite room already exists
            # check room posx/y against room table
                that_room_id = self.database.get_room_if_exists(x=x, y=y, wall_pair=wall_pair)
                print(f"that_room_id = {that_room_id}")
                # room exists if target position exists
            
            #if that_room_id != 0: ### use this
            if that_room_id == 0: ### delete after testing
                that_door = self.database.get_door_from_rwd(room_id=that_room_id, wall_pair=wall_pair)
                print(f"that_door = {that_door}")
                # if exists, check if door can be created
                
                        # look for other room in room_wall_door table
                            # select room_id from room_wall_door
                            # where this_room.this_wall = that_room.pair_of_this_wall


                        # if that_room.door(pair_of_this_wall).room_id = null
                            # create null room
                        # if that_room.door(pair_of_this_wall) = null
                            # create two new doors
                            # that_room.door = new_door(with room = this_room)
                            # this_room.door = new_door(with room = that_room)
                # if other room doesn't exist
                    # check if at room limit
                    # create new door (with last room)
                    # assign new door to new room
                    #print(door_id)
                    #print(room_id)
            

def main():
    test_dungeon = DungeonDB()
    test_dungeon.generate_new_level()
    test_dungeon.generate_new_level(x=10,y=10)
    test_dungeon.generate_room(x=0, y=1)

if __name__ == "__main__":
    main()