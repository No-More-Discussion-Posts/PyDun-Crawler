import pygame
from copd.config import *


class TextBox:

    def __init__(self, width, height, surface, x, y):
        DEFAULT_FONT = pygame.font.get_default_font()
        self.FONT = pygame.font.Font(DEFAULT_FONT, 20)
        self.parent_surface = surface
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def draw(self):
        self.parent_surface.blit(self.surface, (self.x, self.y))

    def add(self, addition, x, y):
        self.surface.blit(addition, (x, y))

    def add_text(self, text, color, pos):
        font = self.FONT.render(text, False, color)
        self.surface.blit(font, pos)

    def add_border(self, color=Colors.BLACK):
        pygame.draw.rect(
            self.surface, color, [0, 0, self.width, self.height], 3, border_radius=15
        )
