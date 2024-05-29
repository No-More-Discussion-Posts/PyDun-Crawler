import pygame
import sys
from dataclasses import dataclass
from enum import Enum
from input_handlers import OPTIONS, Option
from entities import Entity
from typing import Tuple
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


    
            
class BattleMenu():
    def __init__(self,screen,options={}):
        # super().__init__(screen)
        self.screen = screen
        self.options = options
        self.DEFAULT_FONT = pygame.font.get_default_font()
        self.run()

    def run(self):
        self.running = True
        FONT = pygame.font.Font(self.DEFAULT_FONT,20)
        while self.running:
            self.screen.fill("white")
            height = self.screen.get_height();
            width = self.screen.get_width()
            # Create info areas
            monster_info = pygame.draw.rect(self.screen, "black", [10, 10, 200, 100], 3,border_radius = 15)
            player_info = pygame.draw.rect(self.screen,'blue',[width-310,height-210,300,200],3,border_radius = 15)

            # Fill in the details
            monster = Entity("Monster",50)
            player = Entity("Player",100)

            
            
            text = monster.name
            self.screen.blit(FONT.render(text,False,'black'),(20,20))
            self.screen.blit(FONT.render(f"{monster.hp}/{monster.max_hp}",False,"black"),(20,45))
           
           
            pygame.display.flip()  
            for e in pygame.event.get():
                self.handle_input(e)

    def handle_input(self,input) -> None:
            if input.type == pygame.KEYDOWN:
                 if input.key == pygame.K_q:
                      self.running = False
            if input.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

# class InfoBox:
#     def __init__(self,screen,position:Tuple[int,int],height:int=-1,width:int=-1):
#         self.screen = screen
#         self.x, self.y  = position
#         self.FONT_STYLE = pygame.font.get_default_font()
#         self.text = []
#         # self.static_height = True if height != -1 else False
#         # self.static_width = True if width != -1 else False
#         # self.height = 20 if height == -1 else height # 10 px on each side default
#         # self.width = 20 if width == -1 else width # 10 px on each side default
#         self.height = height
#         self.width = width
#         self.text_buffer = 5
#         self.border_buffer = 10


#     def add_text(self,text:str,size : int = 20,color: str = "black") -> None:
#         FONT = pygame.font.Font(self.DEFAULT_FONT,size)
#         new_text = FONT.render(text,False,color)
#         h = new_text.get_height()
#         w = new_text.get_width()
#         # self.height += h + 5 # 5px buffer between text items
#         # self.width = max(self.width, w+20) # Expand width depending on max text size
#         self.text.append(dict(text=new_text,size=(h,w)))

#     def display(self):
#         border = pygame.draw.rect(self.screen, "black", [self.x,self.y, self.width, self.height], 3,border_radius = 15)      
#         x = self.x + self.border_buffer
#         y = self.y + self.border_buffer
#         for text in self.text:
#             self.screen.blit(text['text'],(x,y))
#             self.screen.blit(FONT.render(f"{monster.hp}/{monster.max_hp}",False,"black"),(20,45))
#             x+=text.
