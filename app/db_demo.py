"""
    Simple PyGame window for drawing db visualizations.

"""

import pygame, os, sys
from pytmx.util_pygame import load_pygame
from api import DungeonDB



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
    '''

    # using https://www.youtube.com/watch?v=N6xqCwblyiw as a guide

    ### Starting over with a fresh pygame window while testing pytmx ###
    pygame.init()
    screen = pygame.display.set_mode((MAP_X*16,MAP_Y*16))
    tmx_data = load_pygame('menu.tmx')
    sprite_group = pygame.sprite.Group()

    menu_items = ('COPD: DB DEMO', 'BROWSE TABLES', 'NEW MAP')

    for layer in tmx_data.layers:
        if layer.name in menu_items:

        # if hasattr(layer, 'data'):
             for x, y, surf in layer.tiles():
                 #print(dir(layer))
                 pos = (x * 16, y * 16)
                 Tile(pos = pos, surf = surf, groups = sprite_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        screen.fill('black')
        sprite_group.draw(screen)
        pygame.display.update()




    # game.run()
    # db = DungeonDB()
    # map = db.generate_new_level()
    # print(map)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)


class demo_engine:
    #TODO hook this into the ecs and create a simple map engine
    pass

    if __name__ == "__main__":
        main()