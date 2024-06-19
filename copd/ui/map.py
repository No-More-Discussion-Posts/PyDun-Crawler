
import csv
from pathlib import Path
from copd.engine.entities import Entity
from copd.config import *

class Map:
    def __init__(self,game,filename):
        self.game = game
        self.start_x = 0
        self.start_y = 0
        self.filename = filename

    def read_csv(self):
        map = []
        with open(Path(self.filename)) as data:
            data = csv.reader(data,delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self):
        map = self.read_csv()
        x,y = 0,0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0': # Wall
                    group=self.game.solid_blocks
                    name = "wall"
                elif tile == '1': # Floor
                    group = self.game.blocks
                    name = "floor"
                elif tile == '2': # Door
                    group,name = self.door_or_wall(x,y)

                Entity(self.game,x, y,group=group,name=name).draw()
                x+=1
            y += 1

    def door_or_wall(self,x,y):
        """
#         overworld_map:
#         [0, 0], [1, 0], [2, 0]
#         [0, 1], [1, 1], [2, 1]
#         [0, 2], [1, 2], [2, 2]
#         """
        is_door = True
        if self.game.debug:
            print(f"Door at: {x},{y}./nOverworld: {self.game.player.overworldcoords}")
        # East/West Walls
        if self.game.player.overworldcoords[0] == 0:
            if x == 0:
                is_door = False
        elif self.game.player.overworldcoords[0] == OVERWORLD_WIDTH:
            if x == (X_TILES-1):
                is_door = False
        # North South Walls
        if self.game.player.overworldcoords[1] == 0:
            if y == 0:
                is_door = False
        elif self.game.player.overworldcoords[1] == OVERWORLD_HEIGHT:
            if y == (Y_TILES-1):
                is_door = False
            
        if is_door:
            group = self.game.doors
            name = "door"
        else:
            group = self.game.solid_blocks
            name = "wall"

        return group,name
    