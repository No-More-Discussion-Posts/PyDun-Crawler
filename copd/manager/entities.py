from .engine import Entity
from .components import Position,Velocity

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.add_component(Position(10,10))
        self.add_component(Velocity())
        
