from .engine import Component


@Component
class Position:
    def __init__(self,x:int,y:int):
        super().__init__()
        self.x = x
        self.y = y

@Component
class Velocity:
    
    @property
    def vector(self):
        return self._vector
    
    @vector.setter
    def vector(self,x=0,y=0):
        self._vector = (x,y)




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


