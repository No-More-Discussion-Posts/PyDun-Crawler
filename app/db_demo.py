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
    # map = db.generate_new_level()
    # print(map)

    # using https://www.youtube.com/watch?v=N6xqCwblyiw as a guide

    ### Starting over with a fresh pygame window while testing pytmx ###
    pygame.init()
    menu_state = State.MAIN
    screen = pygame.display.set_mode((MAP_X*16,MAP_Y*16))
    tmx_data = load_pygame('menu.tmx')
    sprite_group = pygame.sprite.Group()
    cursor_group = pygame.sprite.Group()
    map_group = pygame.sprite.Group()

    # print(dir(tmx_data))
    # print(tmx_data)

    map_grid = None
    map_exists = False
    while True:

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:
                click_pos = pygame.mouse.get_pos()
                # print(f"clicking {selection}")
                menu_state = get_state(db=db, state=menu_state, selection=selection)
                if menu_state == State.MAP:
                    # map_grid = get_map_grid(db=db)
                    # print('getting new map')
                    pass
                else:
                    map_grid = None
                    map_exists = False
                # print(menu_state)
                cursor_group.empty()
                map_group.empty()
                sprite_group.empty()
                sprite_group.update()


            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        screen.fill('black')

        selection = None
        cursor = None

        menu_items = get_menu_items(state=menu_state)
        m_pos = pygame.mouse.get_pos()
        # print(m_pos)

        for layer in tmx_data.layers:
            if layer.name in menu_items:

                # cursor = get_cursor(selection)
            #  if hasattr(layer, 'data'):
                # print(m_pos)
                for x, y, surf in layer.tiles():
                    #print(dir(layer))
                    # print(layer)
                    pos = (x * 16, y * 16)

                    # print(f"pos[0]={pos[0]}, pos[1]={pos[1]}, m_pos[0]={m_pos[0]}, m_pos[1]={m_pos[1]}")
                    if (pos[0] <= m_pos[0] <= pos[0]+16) & (pos[1] <= m_pos[1] <= pos[1]+16):
                    #     print(pos)
                        selection = layer.name
                        cursor = get_cursor(selection)
                            # print('HIT')
                        
                    # print(f"pos={pos}, m_pos={m_pos}")
                    Tile(pos = pos, surf = surf, groups = sprite_group)
        # print(selection)
        cursor = get_cursor(selection)
        if cursor is not None:
            c_layer = tmx_data.get_layer_by_name(cursor)
            for x, y, surf in c_layer.tiles():
                pos = (x * 16, y * 16)
                Tile(pos = pos, surf = surf, groups = cursor_group)
        else:
            cursor_group.empty()


        if (menu_state == State.MAP) & (map_exists == False):
            map_grid = get_map_grid(db=db)
            map_layer = tmx_data.get_layer_by_name('MAP GRID')
            for x, y, surf in map_layer.tiles():
                    #print(dir(layer))
                    # print(layer)
                    pos = (x * 16, y * 16)
                    # print(map_grid)
                    # print(f"x={x}, y={y}")
                    if map_grid[y][x-10] != 0: # This is assuming a 20x20 grid, centered
                        # print('map tile found')
                        Tile(pos = pos, surf = surf, groups = map_group)
            map_exists = True

            
        # cursor = get_cursor(selection)
        map_group.draw(screen)
        sprite_group.draw(screen)
        cursor_group.draw(screen)
        pygame.display.update()


def get_mouse_target(layers, m_x, m_y):
    target = None
    for layer in layers:
        pass


def get_map_grid(db:DungeonDB):
    map = db.generate_new_level()
    # print(map)
    return map

def get_menu_items(state):
    menu_items = ['COPD: DB DEMO']
    match (state):
        case State.MAIN:
            add_items = (
                'BROWSE TABLES', 
                'NEW MAP',
                'BACK'
            )
        case State.TABLES:
            add_items = (
                'BACK',
                'roommap', 
                'rwd', 
                'room', 
                'door', 
                'treasure', 
                'wall',
            )
        case State.OUTPUT:
            add_items = (
                'BACK',
                'OUTPUT'
            )
        case State.MAP:
            add_items = (
                'BACK',
                # 'MAP GRID'
            )
        case _:
            add_items = ()
    
    for item in add_items:
        menu_items.append(item)

    return menu_items

def get_cursor(selected=None):
    match (selected):
        case 'BACK':
            return 'back_cursor'
        case 'BROWSE TABLES':
            return 'browse_cursor'
        case 'NEW MAP':
            return 'map_cursor'
        case 'roommap':
            return 'roommap_c'
        case 'rwd':
            return 'rwd_c'
        case 'room':
            return 'room_c'
        case 'door':
            return 'door_c'
        case 'treasure':
            return 'treasure_c'
        case 'wall':
            return'wall_c'
        case _:
            return None

def get_state(db:DungeonDB, state, selection=None):
    match (selection):
        case 'COPD: DB DEMO':
            return State.MAIN
        case 'BACK':
            if state == State.OUTPUT:
                return State.TABLES
            return State.MAIN
        case 'BROWSE TABLES':
            return State.TABLES
        case 'NEW MAP':
            # get_map_grid(db=db)
            # map = db.generate_new_level()
            # print(map)
            return State.MAP
        case 'roommap' | 'rwd' | 'room' | 'door' | 'treasure' | 'wall':
            run_query(selection=selection, db=db)
            return State.OUTPUT
        case _:
            return State.MAIN

def run_query(selection, db:DungeonDB):
    try:
        match (selection):
            case 'roommap':
                results = db.database.get_room_maps()
            case 'rwd':
                results = db.database.get_rwds()
            case 'room':
                results = db.database.get_rooms()
            case 'door':
                results = db.database.get_doors()
            case 'treasure':
                results = db.database.get_treasures()
            case 'wall':
                results = db.database.get_walls()
            case _:
                results = ['Table Not Found']
    except AttributeError as error:
        print(error)
        results = [str(error), f'{selection} table may be empty']
    if len(results) == 0:
        print(f'{selection} table is empty')
    for result in results:
        print(result)

class Tile(pygame.sprite.WeakSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class State(Enum):
    MAIN = 1,
    TABLES = 2,
    OUTPUT = 3,
    MAP = 4,




class demo_engine:
    #TODO hook this into the ecs and create a simple map engine
    pass

    if __name__ == "__main__":
        main()