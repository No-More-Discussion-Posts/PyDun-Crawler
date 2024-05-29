"""Main Game Loop"""
import pygame
from entities import *
from menus import PauseMenu, BattleMenu

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


def main()->None:
    '''Main game loop'''
    pygame.display.set_caption("Dungeon Crawler")
    running = True
    while running:
        screen.fill('white') 
        Test_Grid()
        
        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PauseMenu(screen)
                if event.key == pygame.K_b:
                    BattleMenu(screen)
        pygame.display.update()
    # End game loop
    pygame.quit()

def Test_Grid():
    # draw red rectangle
    pygame.draw.rect(screen, (255, 0, 0), [100, 50, 400, 100], 6)

    #draw lines horizontally
    for x in range(0, 640, 20):
            pygame.draw.line(screen, (128, 128, 128), (x, 0), (x, 360))
    #draw lines vertically
    for y in range(0, 360, 20):
            pygame.draw.line(screen, (128, 128, 128), (0, y), (640, y))
    #draw blue rectangle
    pygame.draw.rect(screen, (0, 0, 255), [50, 100, 400, 100], 6)
   
if __name__ == "__main__":
    main()