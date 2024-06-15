
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
                if tile == '0':
                    group=self.game.solid_blocks
                    name = "wall"
                elif tile == '1':
                    group = self.game.blocks
                    name = "floor"
                elif tile == '2':
                    group = self.game.doors
                    name = "door"

                Entity(self.game,x*TILE_SIZE, y*TILE_SIZE,group=group,name=name).draw()
                x+=1
            y += 1
# def load_start_map(self, color, map=None) -> None:
#         """
#         loads starting map
#         Parameters
#         ----------
#         color: Type: List, RGB value of wall color
#         map: Type: Array, x and y coordinates of map tiles
#         """
#         if map is not None:
#             # accepts alternate map
#             map = map
#         else:
#             # load default starting map
#             map = DEFAULT_MAP

#         # add player to game
#         self.add_player()
#         # add monster sprite to game
#         self.add_monster()
#         # self.Combat.add_entity()
#         # add wall sprites around perimiter of map
#         self.create_walls(map, color)
#         # add treasure sprite to game
#         self.add_treasure(14, 10)

#   def door_or_walls(self):
#         """
#         overworld_map:
#         [0, 0], [1, 0], [2, 0]
#         [0, 1], [1, 1], [2, 1]
#         [0, 2], [1, 2], [2, 2]
#         """

#         # up and down
#         if self.player.overworldcoords[1] == 0:  # if north border
#             Wall(self, 17, 0, Colors.BLUE)  # draw wall at north door
#         else:
#             Door(self, 17, 0)  # draw north door
#         if self.player.overworldcoords[1] == 2:  # if south border
#             Wall(self, 17, 17, Colors.BLUE)  # draw wall at south door
#         else:
#             Door(self, 17, 17)  # draw south door

#         # left and right
#         if self.player.overworldcoords[0] == 0:  # if nwest border
#             Wall(self, 0, 9, Colors.BLUE)  # draw wall at west door
#         else:
#             Door(self, 0, 9)  # draw west door

#         if self.player.overworldcoords[0] == 2:  # if east border
#             Wall(self, 31, 9, Colors.BLUE)  # draw wall at east door
#         else:
#             Door(self, 31, 9)  # draw east door

#     def create_walls(self, map, color):
#         self.doors.empty()
#         self.blocks.empty()
#         for x in map[0]:
#             if x == 17:
#                 # perform check here instead
#                 # Door(self, x, 0) #draw north door
#                 # Door(self, x, 17) #draw south door
#                 self.door_or_walls()
#             else:
#                 Wall(self, x, 0, color)  # draw north wall
#                 Wall(self, x, 17, color)  # draw south wall
#         for y in map[1]:
#             if y == 9:
#                 # Door(self, 0, y) #draw west door
#                 # Door(self, 31, y) #draw east door
#                 self.door_or_walls()
#             else:
#                 Wall(self, 0, y, color)  # draw west wall
#                 Wall(self, 31, y, color)  # draw east wall
#         for x in range(1, 31):
#             for y in range(1, 17):
#                 self.bg = Background(self, x, y)