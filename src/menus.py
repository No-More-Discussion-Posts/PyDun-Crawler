import pygame
# from typing import Tuple, Dict

class Menu:
    def __init__(self,screen):
        self.screen=screen


def pause(screen):
        paused = True
        FONT_FILE = pygame.font.get_default_font()
        FONT = pygame.font.Font(FONT_FILE,24)
        text = FONT.render("PAUSED",False,(255,255,255))

        while paused:
            screen.fill((0,0,0))
            screen.blit(text,(20,20))  
            pygame.display.update()  
            for event in pygame.event.get():
                 if event == pygame.QUIT:
                      pygame.quit()
                              
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                paused = False
            
