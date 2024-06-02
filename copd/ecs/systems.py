from .ecs import System
from .components import Position,Velocity

# class Collision(System):
#     def __init__(self) -> None:
#         pass


class Movement(System):
    
    def update(self):
        for entity in self.entities:
            entity.get(Position)+entity.get(Velocity)
            