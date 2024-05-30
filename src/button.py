import pygame

class Button:
    def __init__(self, name:str, game, x:int, y:int,on_click = None):
        """Simple Button

        Args:
            name (str): Text to be displayed 
            game (Engine): Main game instance
            x (int): top left x position 
            y (int): top left y position
            on_click (_type_, optional): Function to be run when clicked. Defaults to None.
        """    
        self.DEFAULT_FONT = pygame.font.get_default_font()
        FONT = pygame.font.Font(self.DEFAULT_FONT, 20)
        self.game = game
        self.button_surface = pygame.Surface((135, 60))
        self.text = FONT.render(name, True, (255, 255, 255))
        self.rect = self.text.get_rect(
            center=(
                self.button_surface.get_width() / 2,
                self.button_surface.get_height() / 2,
            )
        )
        self.butt_rect = pygame.Rect(x, y, 135, 60)
        self.button_surface.blit(self.text, self.rect)
        self.game.screen.blit(self.button_surface, (self.butt_rect.x, self.butt_rect.y))
        self.on_click = on_click
    
    def set_on_click(self,action):
        self.on_click = action

    def click(self):
        self.on_click()
    
    def collidepoint(self,pos):
        return self.butt_rect.collidepoint(pos)