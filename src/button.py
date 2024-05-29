import pygame

class button:
    def __init__(self, name, x, y):
        self.DEFAULT_FONT = pygame.font.get_default_font()
        FONT = pygame.font.Font(self.DEFAULT_FONT,20)
        self.button_surface = pygame.Surface((135, 60))
        self.text = FONT.render(name, True, (255, 255, 255))
        self.rect = self.text.get_rect(center=(self.button_surface.get_width()/2, self.button_surface.get_height()/2))
        self.butt_rect = pygame.Rect(x, y, 135, 60)