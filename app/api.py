"""
    Internal API with endpoints for game data.
"""

import random
import csv
import yaml
from db import DB
from db import Room
from sqlalchemy import *
from sqlalchemy.orm import *
from yaml import CLoader
from pathlib import Path

MAP_X = 20
MAP_Y = 20
ROOM_LIMIT = 20
ROOM_MINIMUM = 10

engine = create_engine("sqlite://", echo=True)
database = DB()

#TODO: read csv, load tile map into db, tile object, 
# add xy for tile positions in room
# get all tiles that match room id
# return a list of room objects


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

        self.max_rooms = ROOM_LIMIT
        self.min_rooms = ROOM_MINIMUM


        #TODO: put csv file paths in yaml file
        #TODO: write method to read yaml
        #TODO: write method to load csv files into db


    def load_files(self):
        FILE_PATH = "files.yaml"

        yaml_file = Path(FILE_PATH)
        self.files = yaml.load(yaml_file.read_text(), CLoader)
        print_gaps(self.files)
        room_maps = self.files['room_map']
        #print_gaps(room_maps)

        # These can be loaded in bulk
        for room_map in room_maps:
            filename = room_maps[room_map]
            # print(filename)
            map_string = ""
            with open(filename) as map_file:
                map_reader = csv.reader(map_file)
                for line in map_reader:
                    row = ",".join(line)
                    print(row)
                    map_string += f"{row}|"
            #print(map_string)
            #print(f"length = {len(map_string)}\n")
            map_id = self.database.create_room_map(map_string=map_string)
            # print(self.database.read_room_map(id=map_id))

    # basic level generation sequence:
    def generate_new_level(
            self,
            x=MAP_X,
            y=MAP_Y,
            max_rooms=ROOM_LIMIT,
            min_rooms=ROOM_MINIMUM) -> None:
        self.room_count = 0
        self.max_rooms = max_rooms
        self.min_rooms = min_rooms
        
        # create 2d array
        self.map_coords = [[*range(x)],[*range(y)]]
        #print(map_coords)
        map_array = [[0 for row in self.map_coords[0]] for col in self.map_coords[1]]
        
        # pick a random seed room (this will be "room 0")
        #seed_x = random.choice(self.map_coords[0])
        #seed_y = random.choice(self.map_coords[1])
        seed_x = x//2
        seed_y = y//2
        # map_array[seed_y][seed_x] = 1
        #print(map_array)
        # print(f"seed room = {seed_x},{seed_y}")

        self.walls = self.generate_walls()

        # while self.room_count < ROOM_MINIMUM:        
        #     self.generate_map(x=seed_x, y=seed_y)
        #     self.room_count = len(self.database.get_rooms())
            
        self.generate_map(x=seed_x, y=seed_y)


        ### If the count comes up short, try again up to three times ###
        #TODO: This isn't doing anything any more. To fix it,
        # the tables need to be dropped before trying again.

        # if self.room_count < ROOM_MINIMUM:
        #     self.generate_map(x=seed_x, y=seed_y)

        # if self.room_count < ROOM_MINIMUM:
        #     self.generate_map(x=seed_x, y=seed_y)

        # if self.room_count < ROOM_MINIMUM:
        #     self.generate_map(x=seed_x, y=seed_y)
           
        all_rooms = self.database.get_rooms()
        #print_gaps("rooms: ")
        #print_gaps(f"first room: {first_room}")
        for room in all_rooms:
            # print(room)
            # print(self.database.get_room_map(room.id))
            # map_array[room.y][room.x] = 1
            map_array[room.y][room.x] = room.id
            # print_gaps(self.database.get_room_neighbors(room_id=room.id))
            self.generate_doors(room.id)

        all_rwds = self.database.get_rwds()
        for rwd in all_rwds:
            # print(rwd)
            pass

        # print("\nMAP:")
        # for row in map_array:
        #     print(row)
        # print()

        # TODO: pick a random room to declare as exit?

        return map_array


    # Create a grid of room_ids:
    #   Create room
    #   Shuffle "walls"
    #   Iterate through walls:
    #       if opposite room is out of bounds, return
    #       if opposite room exists, return
    #       if adding a room, recur
    #     
    # Iterate through grid:
    #   Create four RWDs for each room
    #   Check if room has adjacent rooms <-- doing now
    #       Create doors and update RWDs


    # map grid generation sequence
    # do it recursively this time
    def generate_map(self, x, y):
        self.room_count = len(self.database.get_rooms())
        print_gaps(self.room_count)
        if self.room_count >= self.max_rooms:
            return
        
        if self.database.room_exists(x=x, y=y):
            return
        
        new_room = self.database.create_room(x=x, y=y)
        print_gaps(new_room)
        random_map = random.randint(1,2)
        self.database.add_room_map_to_room(room_id=new_room, room_map_id=random_map)

        # walls = self.generate_walls()
        random.shuffle(self.walls)
        for wall in self.walls:
            print_gaps(f"wall = {wall}")
            match (wall): # same switch exists on db.py (but 1 indexed)
                # facing....
                case 0: # north
                    y -= 1
                case 1: # east
                    x += 1
                case 2: # south
                    y += 1
                case 3: # west
                    x -= 1
                    
            # if self.database.room_exists(x=x, y=y):
            #     return

            if not self.room_in_bounds(x=x, y=y):
                return
            
            if (self.room_count > self.min_rooms) & (random.randint(0,4) == 0):
                return
            
            self.generate_map(x=x, y=y)


    def generate_walls(self):
         # randomise wall choice
        walls = list(range(4))
        random.shuffle(walls)
        print_gaps(f"walls = {walls}")
        return walls
    
    def generate_doors(self, room_id):
        neighbors = self.database.get_room_neighbors(room_id=room_id)
        print_gaps(neighbors)
        for neighbor in neighbors:
            if neighbor[0] > 0:
                print_gaps(neighbor)
                new_door = self.database.create_door(room_id=neighbor[0])
                self.database.add_rwd_door_from_room(
                    room_id=room_id,
                    wall=neighbor[1],
                    door_id=new_door
                )


    # Helper methods
    def room_in_bounds(self, x, y) -> Boolean:
        x_valid = self.map_coords[0].count(x) > 0
        y_valid = self.map_coords[1].count(y) > 0
        return x_valid & y_valid
    

    # Retrieval methods
    def get_map_from_room(self, room_id):
        """_summary_

        Args:
            room_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.database.get_room_map(room_id=room_id)

    def get_level_grid(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        map_array = [[0 for row in self.map_coords[0]] for col in self.map_coords[1]]
        all_rooms = self.database.get_rooms()
        #print_gaps("rooms: ")
        #print_gaps(f"first room: {first_room}")
        for room in all_rooms:
            # print(room)
            # print(self.database.get_room_map(room.id))
            # map_array[room.y][room.x] = 1
            map_array[room.y][room.x] = room.id
            # print_gaps(self.database.get_room_neighbors(room_id=room.id))
            #self.generate_doors(room.id)
        return map_array

def print_gaps(str):
    # print (f"\n -- {str} -- \n")
    pass

def main():
    test_dungeon = DungeonDB()
    test_dungeon.load_files()
    test_dungeon.generate_new_level()
    #test_dungeon.generate_new_level(x=10,y=10)
    #test_dungeon.generate_room(x=0, y=1)
    print(test_dungeon.get_level_grid())

if __name__ == "__main__":
    main()
