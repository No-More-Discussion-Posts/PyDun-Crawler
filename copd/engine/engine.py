from enum import Enum

class Components(Enum):
    POSITION = 1
    VELOCITY = 2

class Entity():
    '''
    Distinct Object
    '''
    components = []
    def __init__(self):
        pass


    def add_component(self,component):
        pass
    
    def remove_component(self,component):
        pass
    
    def get_component(self,component):
        pass

    def get_components(self,components):
        return [self.get_component(c) for c in components]


class Component:
    pass


class System():
    '''
    Functions behind the components
    '''
    systems = []
    database = {}

    def __init__(self) -> None:
        if type(self) in System.database:
            raise Exception('Duplicate system types')
        System.systems.append(self)
        System.database[type(self)] = self

    @classmethod
    def update_all(cls):
        for system in cls.systems:
            system.update()

    def update(self):
        pass
        
