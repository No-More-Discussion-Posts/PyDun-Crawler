import pygame
from typing import Tuple, Dict
import sys

class Menu:
    def __init__(self,screen):
        self.screen=screen


def pause(screen,options:Dict = {}):
        paused = True
        caption = pygame.display.get_caption()
        if 'caption' in options:
             pygame.display.set_caption(options['caption'])
        FONT_FILE = pygame.font.get_default_font()
        FONT = pygame.font.Font(FONT_FILE,24)
        text = FONT.render("PAUSED",False,(255,255,255))
        
        while paused:
            screen.fill((0,0,0))
            screen.blit(text,(20,20))  
            pygame.display.update()  
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                      pygame.quit()
                      sys.exit()
                elif e.type == pygame.KEYDOWN:
                     if e.key == pygame.K_p:
                        paused = False
        pygame.display.set_caption(caption[0])
            
