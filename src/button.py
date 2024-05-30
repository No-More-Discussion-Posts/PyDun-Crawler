import pygame

class button:
    def __init__(self, name, game, x, y):
        self.DEFAULT_FONT = pygame.font.get_default_font()
        FONT = pygame.font.Font(self.DEFAULT_FONT,20)
        self.game = game
        self.button_surface = pygame.Surface((135, 60))
        self.text = FONT.render(name, True, (255, 255, 255))
        self.rect = self.text.get_rect(center=(self.button_surface.get_width()/2, self.button_surface.get_height()/2))
        self.butt_rect = pygame.Rect(x, y, 135, 60)
    def show(self):
        self.button_surface.blit(self.text, self.rect)
        self.game.screen.blit(self.button_surface, (self.butt_rect.x, self.butt_rect.y))

