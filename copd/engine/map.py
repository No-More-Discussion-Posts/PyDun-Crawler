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