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
    # character_group = pygame.sprite.Group()

    # print(dir(tmx_data))
    # print(tmx_data)

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # print(event.dict)
                print(pygame.key.name(event.key))
                print(pygame.key.key_code(pygame.key.name(event.key)))
                demo_state = get_state(key=event.key)
                print(demo_state)
                sprite_group.empty()
            
        # character_group.empty()
        # character_group.update()
        screen.fill('black')

        # selection = None
        display_items = get_display_items(state=demo_state, db=db)
        print(display_items)
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
                    # pos = (x * 16, y * 16)
                    # selection = layer.name
                    if layer.name in ('blobi','hobgoblin','goblin','ogre'):
                        # print("\nFOUND\n")
                        pos = (0, 0)
                        RunningTile(pos=pos, surf=surf, groups=character_group, character=layer.name)
                    else:
                        Tile(pos = pos, surf = surf, groups = sprite_group)


                    
            
        sprite_group.draw(screen)
        character_group.draw(screen)
        
        pygame.display.update()

        clock.tick(10)
        print('tick')

def get_mouse_target(layers, m_x, m_y):
    target = None
    for layer in layers:
        pass

def get_map_grid(db:DungeonDB):
    # map = db.generate_new_level()
    # print(map)
    # return map
    pass

def get_character():
    pass

def get_display_items(state, db:DungeonDB):
    # return db.get_scene('title')
    match(state):
        case State.INTRO:
            scene = db.get_scene('title')
            # print(scene)
            return scene
        case State.DUNGEON:
            pass
        case State.MAP:
            pass
        case State.PAUSE:
            pass
        case State.COMBAT:
            scene = db.get_scene('combat')
            # print(scene)
            # return scene
            return get_combat_items(scene=scene, monster='goblin')
        case State.WIN:
            pass
        case State.GAMEOVER:
            pass
        case State.SETTINGS:
            pass
        # case State.TR_0:
        #     return db.get_scene('room0')
        case State.TR_1:
            return db.get_scene('room1')
        case State.TR_2:
            return db.get_scene('room2')
        case State.TR_3:
            return db.get_scene('room3')
        case State.TR_4:
            return db.get_scene('room4')
        case State.TR_5:
            return db.get_scene('room5')
        case State.TR_6:
            return db.get_scene('room6')
        case State.TR_7:
            return db.get_scene('room7')
        case State.TR_8:
            return db.get_scene('room8')
        case State.TR_9:
            return db.get_scene('room9')
        case _:
            return []

def get_cursor(selected=None):
    pass
        
def get_state(key, state=None):
    match(key):
        case pygame.K_0:
            return State.INTRO
        case pygame.K_1:
            return State.TR_1
        case pygame.K_2:
            return State.TR_2
        case pygame.K_3:
            return State.TR_3
        case pygame.K_4:
            return State.TR_4
        case pygame.K_5:
            return State.TR_5
        case pygame.K_6:
            return State.TR_6
        case pygame.K_7:
            return State.TR_7
        case pygame.K_8:
            return State.TR_8
        case pygame.K_9:
            return State.TR_9
        case pygame.K_c:
            return State.COMBAT

def run_query(selection, db:DungeonDB):
    pass

def get_combat_items(scene, monster, player=None):
    prefix = 'cm_'
    postfix = '_hp'
    layers = []
    for layer in scene:
        # print(f"layer={layer}")
        if prefix not in layer: # no "cm_" (combat mob) in layer name
            layers.append(layer)
            continue
        if ((prefix + monster) in layer) | ((prefix+monster+postfix) in layer):
            layers.append(layer)
    return layers


class Tile(pygame.sprite.WeakSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        

# https://www.simplifiedpython.net/pygame-sprite-animation-tutorial/
# reference ^
class RunningTile(Tile):
    def __init__(self, pos, surf, groups, character:str):
        super().__init__(pos=pos, surf=surf, groups=groups)
        self.MAX_X = 5
        self.image = surf
        self.rects = []
        self.index = 0
        self.y = 0
        match(character):
            case 'blobi':
                self.y = 0
            case 'hobgoblin':
                self.y = 1
            case 'goblin':
                self.y = 2
            case 'ogre':
                self.y = 3
        for i in range(0, self.MAX_X):
            frame = (i*16,self.y*16)
            self.rects.append(self.image.get_rect(topleft = frame))


    def update(self):
        self.index += 1

        if self.index >= self.MAX_X:
            self.index = 0

        self.rect = self.rects[self.index]

    def get_rect(self):
        print('get_rect')
        return self.rect
        
        

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
    TR_0 = 10,
    TR_1 = 11,
    TR_2 = 12,
    TR_3 = 13,
    TR_4 = 14,
    TR_5 = 15,
    TR_6 = 16,
    TR_7 = 17,
    TR_8 = 18,
    TR_9 = 19,


def get_key_screen(key):
    pass
            



class demo_engine:
    #TODO hook this into the ecs and create a simple map engine
    pass

    if __name__ == "__main__":
        main()