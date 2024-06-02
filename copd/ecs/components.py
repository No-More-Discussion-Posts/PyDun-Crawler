import pygame
from .ecs import Component


        

class Position(Component):
    def __init__(self,x:int,y:int):
        super().__init__()
        self.x = x
        self.y = y

    def __add__(self,obj):
        if isinstance(obj, Velocity):
            self.x += obj.dx
            self.y += obj.dy
        else:
            raise TypeError("Position must be incremented with a Velocity object")
        return self
    def __str__(self):
        return f"Position - x:{self.x}, y:{self.y}"
    
    def __repr__(self):
        return f"Position - x:{self.x}, y:{self.y}"

class Velocity(Component):
    
    def __init__(self,dx:int=0,dy:int=0):
        self.dx = dx
        self.dy = dy
    
    def set_from_key(self,key):
        match key:
            case pygame.K_w:
                self.dx = 0
                self.dy = -1
            case pygame.K_s:
                self.dx = 0
                self.dy = 1
            case pygame.K_a:
                self.dx = -1
                self.dy = 0
            case pygame.K_d:
                self.dx = 1
                self.dy = 0

    def set(self,dx,dy):
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return f"Velocity - dx:{self.dx}, dy:{self.dy}"
    
    def __repr__(self):
        return f"Velocity - dx:{self.dx}, dy:{self.dy}"

# class HitPoints(Component):

# @Component
# class Mobile:
#     def __init__(self) -> None:
#         pass

#     def move_up(self):
#         pass

#     def move_down(self):
#         pass

#     def move_left(self):
#         pass

#     def move_right(self):
#         pass

#     def move(self,x,y):
#         pass


