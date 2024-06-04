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
        if key == pygame.K_w:
            self.dx = 0
            self.dy = -1
        elif key == pygame.K_s:
            self.dx = 0
            self.dy = 1
        elif key ==  pygame.K_a:
            self.dx = -1
            self.dy = 0
        elif key == pygame.K_d:
            self.dx = 1
            self.dy = 0

    def set(self,dx,dy):
        self.p_dx = self.dx
        self.p_dy = self.dy
        self.dx = dx
        self.dy = dy

    def previous(self):
        return Velocity(self.p_dx,self.p_dy)
    def __str__(self):
        return f"Velocity - dx:{self.dx}, dy:{self.dy}"
    
    def __repr__(self):
        return f"Velocity - dx:{self.dx}, dy:{self.dy}"
    

class TurnCounter(Component):
    def __init__(self):
        self.turn = 0

class HitPoints(Component):
    def __init__(self,max_hp=-1,hp=-1):
        self.max_hp = max_hp
        self.hp = hp 

    

