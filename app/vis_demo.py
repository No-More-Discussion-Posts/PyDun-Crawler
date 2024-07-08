"""
    Simple PyGame window for drawing db visualizations.

"""

import pygame, os, sys
from pytmx.util_pygame import load_pygame
from api import DungeonDB
from enum import Enum


# if "copd" not in sys.modules:
#     parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#     print(f"Adding: {parent_dir_name}")
#     sys.path.append(parent_dir_name)
# from copd.engine import Engine
# from copd.ui.tiles import Map

MAP_X = 40
MAP_Y = 20

def create_demo_map(x, y):
    map = [[*range(x)],[*range(y)]]
    print(map)
    return map
        
def main() -> None:
    """Main "game" loop"""
    '''
    game = Engine()
    #game.load_start_map((0, 0, 255), map=DEFAULT_MAP)

    map = create_demo_map(MAP_X, MAP_Y)
    #game.load_start_map(color=(0, 0, 255))

    map = Map(game=game, filename='./app/demomap.csv')
    game.load_start_map(color=(0, 0, 255), map=map)

    game.Test_Grid()
    game.run()
    '''
    db = DungeonDB()
    db.load_files()
    # map = db.generate_new_level()
    # print(map)

    # using https://www.youtube.com/watch?v=N6xqCwblyiw as a guide

    ### Starting over with a fresh pygame window while testing pytmx ###
    pygame.init()
    demo_state = State.INTRO
    screen = pygame.display.set_mode((MAP_X*16,MAP_Y*16))
    tmx_data = load_pygame('basic_room.tmx')
    sprite_group = pygame.sprite.Group()

    # print(dir(tmx_data))
    # print(tmx_data)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        screen.fill('black')

        # selection = None
        print(demo_state)
        display_items = get_display_items(state=demo_state, db=db)
        # m_pos = pygame.mouse.get_pos()
        # print(m_pos)

        for layer in tmx_data.layers:
            '''
            '''
            # [print(display_items)]
            if layer.name in display_items:
                # print('Found!')

                # cursor = get_cursor(selection)
            #  if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    #print(dir(layer))
                    # print(layer)
                    pos = (x * 16, y * 16)
                    # selection = layer.name
                    Tile(pos = pos, surf = surf, groups = sprite_group)
        
        sprite_group.draw(screen)
        pygame.display.update()


def get_mouse_target(layers, m_x, m_y):
    target = None
    for layer in layers:
        pass

def get_map_grid(db:DungeonDB):
    # map = db.generate_new_level()
    # print(map)
    # return map
    pass

def get_display_items(state, db:DungeonDB):
    # match(state):
    #     case State.INTRO:
    #         scene = db.get_scene('title')
    #         # print(scene)
    #         return scene
    return db.get_scene('title')

def get_cursor(selected=None):
    pass
        
def get_state(db:DungeonDB, state, selection=None):
    pass

def run_query(selection, db:DungeonDB):
    pass

class Tile(pygame.sprite.WeakSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class State(Enum):
    MAIN = 1,
    INTRO = 2,
    DUNGEON = 3,
    MAP = 4,
    PAUSE = 5,
    COMBAT = 6,
    WIN = 7,
    GAMEOVER = 8,
    SETTINGS = 9

class DungeonState(Enum):
    ONE = 1,
    TWO = 2,
    THREE = 3,
    FOUR = 4,
    FIVE = 5,
    SIX = 6,
    SEVEN = 7,
    EIGHT = 8,
    NINE = 9,


class demo_engine:
    #TODO hook this into the ecs and create a simple map engine
    pass

    if __name__ == "__main__":
        main()