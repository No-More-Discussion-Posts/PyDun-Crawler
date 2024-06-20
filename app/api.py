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

        self.max_rooms = ROOM_LIMIT

    # TODO: create dungeon map generator

    # this needs to return a 2d array of room_ids
    # each room_id must correspond to a unique room object

    # basic dun gen sequence:
    
    def generate_new_level(self, x=MAP_X, y=MAP_Y, size=ROOM_LIMIT) -> None:
        self.max_rooms = size
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
        room_count = 0
        last_door = 0
        while (room_count < size):
            room_count += 1 # thanks, sql
            if (room_count == 1):
                last_door = self.generate_room(
                    x=seed_x,
                    y=seed_y,
                )
            else:
                last_door = self.generate_room(
                    last_door=last_door
                )
            
            

        # Testing 
        first_room = self.database.read_room()
        all_rooms = self.database.get_rooms()
        all_rwds = self.database.get_rwds()
        print("rooms: ")
        print(f"first room: {first_room}")
        for room in all_rooms:
            print(room)
        for rwd in all_rwds:
            print(rwd)

        # pick a random? room to declare as exit

        
    # room gen sequence
    def generate_room(self, x=None, y=None, first_wall=None, last_door=None, room_id=None):
        # create new room
        if last_door is None:
            room_id = 1
            # TODO decide what to do with this:
            #test_room_id = self.database.create_room(0, 0, 0)
            room_id = self.database.create_room(id=room_id, x=x, y=y)
            first_wall = random.randint(0,3)
        else:
            #TODO: FIGURE OUT WHY THIS IS RETURNING NULL:
            last_room_id = self.database.get_room_from_door(last_door)
            first_wall = self.database.get_wall_from_door(door_id=last_door)
            if x is None or y is None:
                #last_room = self.database.read_room(last_room_id)
                #x = last_room.get("x")
                #y = last_room.get("y")
                last_xy = self.database.get_xy_from_room(last_room_id)
                x = last_xy.get("x")
                y = last_xy.get("y")
                print(f"last x = {x}")
                print(f"last y = {y}")
                match (first_wall): # same switch exists on db.py
                # facing....
                    case 0: # north
                        y -= 1
                    case 1: # east
                        x += 1
                    case 2: # south
                        y += 1
                    case 3: # west
                        x -= 1
            #last_room = self.database.read_room(last_room_id)
            room_id = self.database.create_room(id=last_room_id, x=x, y=y)
        

        # No first wall implies seed room (TODO: enforce this somehow)
        # assign random first wall
        if last_door is None:
            first_wall = random.randint(0,3)
        else:
            first_wall = self.database.get_wall_from_door(door_id=last_door)
        print(f"first_wall: {first_wall}")
        
        # randomise wall choice
        walls = list(range(4))
        random.shuffle(walls)
        walls.insert(0, walls.pop(walls.index(first_wall)))
        print(f"walls = {walls}")
                
        ### ALGO NOTES: ###
        ### ADD NEW ROOM ###

        ### create a new set of room_wall_doors ###
        doors = []
        for wall in walls:
            ### randomly decide which walls get a door ###
            if walls.index(wall) == 0:
                door_choice = 1
            else:
                door_choice = random.randint(-1,1)

            ### choose between no, maybe, or yes ###
            ### no = null room (door with null room_id) ###
            ### maybe = null ###
            ### yes = door (with not room) ###

            door_id = None # maybe door
            if door_choice != 0:
                ### create new door with room.id = null ###
                door_id = self.database.create_door()

                if (last_door is not None) & (door_choice == 1):
                    print(f"last room id: {last_room_id}")
                    # TODO write update door method
                    self.database.update_door(door_id=door_id, room_id=room_id)
            

            ### this.door_id = new_door.id  ###
            rwd_id = self.database.create_room_wall_door(room_id=room_id, wall_id=wall, door_id=door_id)
            #door_id = self.database.create_door(room_id=room_id) # door.
            print(rwd_id)
            ### if "no door", don't update door ###
            ### if "yes door" ###
            doors.append({
                'wall':wall,
                'door_choice':door_choice,
                'door_id':door_id,
                'rwd_id':rwd_id,
                'room_id':room_id,
            })
        
        for door in doors:
            wall = door.get('wall')
            door_choice = door.get('door_choice')
            door_id = door.get('door_id')
            rwd_id = door.get('rwd_id')
            room_id = door.get('room_id')

            # yes, this wall-pair system is a bit over-engineered
            # but just imagine if we needed to change
            # the room shape at some point down the line
            wall_pair = self.database.get_opposite_wall(wall) 
            print(f"wall = {wall}, pair = {wall_pair}")
            
            that_room_id = 0 # invalid room (should start at 1)
            
            # door_choice == 1 # For testing
            if door_choice == 1:
                #pass
                
                ### check if opposite room already exists ###
                ### check room posx/y against room table ###
                that_room_id = self.database.get_room_if_exists(x=x, y=y, wall_pair=wall_pair)
                print(f"that_room_id = {that_room_id}")
                ### room exists if target position exists ###
            
            ### if exists, check if door can be created ###
            that_door = None
            if that_room_id != 0: # <--- USE THIS
            #if that_room_id == 0: # <--- DELETE THIS AFTER WRITING
                ### look for other room in room_wall_door table ###
                    ### select room_id from room_wall_door ###
                    ### where this_room.this_wall = that_room.pair_of_this_wall ###

                #that_door = self.database.get_door_from_rwd(room_id=that_room_id, wall_pair=wall_pair)
                that_door = self.database.get_door_from_rwd(room_id=that_room_id, wall_pair=wall_pair)
                print(f"that_door = {that_door}")

            if that_door is not None: # aka, room has door
                pass

                ### if that_room.door(pair_of_this_wall).room_id = null ###
                ### create null room ###
                ### aka, do nothing. it was created ealier ###S

            else:
                ### if that_room.door(pair_of_this_wall) = null ###
                #pass
                ### create two new doors ###
                ### that_room.door = new_door(with room = this_room) ###
                ### this_room.door = new_door(with room = that_room) ###

                # TODO: GO THROUGH THIS WHOLE THING AND MAKE SURE DOOR.ROOM_ID IS CORRECT
                this_new_door_id = self.database.create_door(room_id=that_room_id)
                that_new_door_id = self.database.create_door(room_id=room_id)
                print(f"New door: {this_new_door_id}")
                print(f"New door: {that_new_door_id}")

                ### update room_wall_doors ###
                this_rwd_id = self.database.add_rwd_door_from_room(
                    room_id=room_id,
                    wall=wall,
                    door_id=this_new_door_id
                )
                that_rwd_id = self.database.add_rwd_door_from_room(
                    room_id=that_room_id,
                    wall=wall_pair,
                    door_id=that_new_door_id
                )
                print(this_rwd_id)
                print(that_rwd_id)

            ### if other room doesn't exist ###
            if that_room_id == 0:
                ### check if at room limit ###
                room_count = self.database.get_room_count()
                print(f"room count: {room_count}")

                if room_count < self.max_rooms:
                    #pass
                    ### create new door (with this room) ###
                    new_door_id = self.database.create_door(room_id=room_id)
                    ### assign new door new room rwd ###
                    new_rwd = self.database.create_room_wall_door(
                        room_id=(room_count + 1), # the next room_id
                        door_id=new_door_id,
                        wall_id=wall_pair
                    )
                    print(f"new rwd = {new_rwd}")
                    print(f"returned door = {new_door_id}")
                    return new_door_id
                #print(door_id)
                #print(room_id)
        return None # no last door

def main():
    test_dungeon = DungeonDB()
    test_dungeon.generate_new_level()
    #test_dungeon.generate_new_level(x=10,y=10)
    #test_dungeon.generate_room(x=0, y=1)

if __name__ == "__main__":
    main()

