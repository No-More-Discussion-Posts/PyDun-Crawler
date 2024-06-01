from .engine import System, Components

@System
class Collision:
    def __init__(self) -> None:
        pass


@System
class Movement:
    
    def update(self):
        for entity in self.entities:
            pos,vel = entity.get_components([Components.POSITION,Components.VELOCITY])
            pos += vel
