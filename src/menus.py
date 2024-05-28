import pygame
import sys
from dataclasses import dataclass
from enum import Enum
from input_handlers import OPTIONS, Option

class Menu:
    def __init__(self,screen,options):
        self.screen=screen
        self.options = options
        self.previous_caption = pygame.display.get_caption()[0] 
        self.DEFAULT_FONT = pygame.font.get_default_font()
        self.runnable_opts = []
        self.handlers = []

    def handle_options(self) -> None:
        for option in self.options:
            if option.type == OPTIONS.CAPTION:
                pygame.display.set_caption(option.data)
            elif option.type == OPTIONS.PRINT:
                size = option.data['size']
                text = option.data['text']
                pos = option.data['pos']
                font = option.data['font'] if 'font' in option.data else self.DEFAULT_FONT
                FONT = pygame.font.Font(font,size)
                self.runnable_opts.append(lambda: self.screen.blit(FONT.render(text,False,(255,255,255)),pos))
            elif option.type == OPTIONS.HANDLER:
                 event_type = option.data.get('event_type')
                 if event_type in [pygame.KEYDOWN,pygame.KEYUP]:
                    key = option.data.get('key')
                    result = option.data.get("result")
                    self.handlers.append({'type':event_type,'func':lambda x: result() if x.key == key else ...})

    def handle_input(self,input) -> None:
            for handler in self.handlers:
                if input.type == handler['type']:
                    handler['func'](input)
            if input.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def run_opts(self) -> None:
        for opt in self.runnable_opts:
            opt()
    
    def stop(self) -> None:
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.screen.fill((0,0,0))
            self.run_opts() 
            pygame.display.update()  
            for e in pygame.event.get():
                self.handle_input(e)


    def __del__(self):
        '''Close operations for Menu class'''
        pygame.display.set_caption(self.previous_caption)

class PauseMenu(Menu):
    def __init__(self,screen,options=[]):
        super().__init__(screen,options)
        self.options = options
        self.options.append(Option(OPTIONS.CAPTION,"Paused"))
        self.options.append(Option(OPTIONS.PRINT, dict(
                                                  size = 20,
                                                  text = "PAUSED",
                                                  pos = (100,100),
                                                  )))
        self.options.append(Option(OPTIONS.HANDLER, dict(event_type = pygame.KEYDOWN,
                                                        key = pygame.K_p,
                                                        result = lambda: self.stop(),
                                                        )))
        self.handle_options()
        self.run()


    
            
class BattleMenu(Menu):
    def __init__(self,screen,options={}):
        super().__init__(screen)
        self.options = options