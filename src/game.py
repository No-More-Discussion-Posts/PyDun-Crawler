"""Main Game Loop"""
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


def main()->None:
    '''Main game loop'''
    running = True
    while running:
        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            running = False
        screen.fill((255,255,255))
    pygame.quit()


if __name__ == "__main__":
    main()