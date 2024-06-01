from .engine import Component


# class WASDComponent(Component):
#     def __init__(self):
#         pass

#     def update(self):
#         #update velocity
#         pass
        

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
    
    def __repr__(self):
        return f"Position - x:{self.x}, y:{self.y}"

class Velocity(Component):
    
    def __init__(self,dx:int=0,dy:int=0):
        self.dx = dx
        self.dy = dy

    def __repr__(self):
        return f"Velocity - dx:{self.dx}, dy:{self.dy}"


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


