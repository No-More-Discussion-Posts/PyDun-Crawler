"""Main Game Loop"""
import pygame
from menus import PauseMenu
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Colors. Move to separate file or use a color package in the future
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BG_COLOR = BLACK
def main()->None:
    '''Main game loop'''
    pygame.display.set_caption("Dungeon Crawler")
    running = True
    while running:
        events = pygame.event.get()
        screen.fill(BG_COLOR)
        pygame.draw.circle(screen,"red",(SCREEN_WIDTH/2,SCREEN_HEIGHT/2),20)
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # pause(screen,dict(caption="Paused"))
                    PauseMenu(screen,dict(caption="Paused"))
        pygame.display.update()
    # End game loop
    pygame.quit()

if __name__ == "__main__":
    main()