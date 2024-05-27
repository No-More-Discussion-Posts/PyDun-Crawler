'''Game Entry Point'''
import tcod
import os
from entity import Entity
from input_handlers import EventHandler
from engine import Engine

FONT = os.path.join(os.path.dirname(__file__),"assets","dejavu10x10_gs_tc.png")
def main():
    '''
    Main game loop
    '''
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(FONT,32, 8, tcod.tileset.CHARMAP_TCOD)
    
    event_handler = EventHandler()

    player = Entity(int(screen_width / 2),int(screen_height / 2), "@",(255,255,255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@",(255,255,0))
    entities = {npc,player}
    engine = Engine(entities=entities,event_handler=event_handler,player=player)
    
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Dungeon Crawler",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()
