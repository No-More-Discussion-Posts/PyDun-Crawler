import pygame
from typing import Tuple, Dict
import sys

class Menu:
    def __init__(self,screen):
        self.screen=screen
        self.previous_caption = pygame.display.get_caption()[0] 

    def __del__(self):
        pygame.display.set_caption(self.previous_caption)

class PauseMenu(Menu):
    def __init__(self,screen,options):
        super().__init__(screen)
        self.options = options
        
        self.run()

    def run(self):
        screen = self.screen
        running = True
        if 'caption' in self.options:
             pygame.display.set_caption(self.options['caption'])
        FONT_FILE = pygame.font.get_default_font()
        FONT = pygame.font.Font(FONT_FILE,24)
        text = FONT.render("PAUSED",False,(255,255,255))
        
        while running:
            screen.fill((0,0,0))
            screen.blit(text,(20,20))  
            pygame.display.update()  
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                      pygame.quit()
                      sys.exit()
                elif e.type == pygame.KEYDOWN:
                     if e.key == pygame.K_p:
                        running = False

    
            
