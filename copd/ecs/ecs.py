class Entity():
    '''
    Distinct Object
    '''
    
    def __init__(self):
        self.components = {}


    def add_component(self,component):
        self.components[type(component)] = component
    
    def remove_component(self,component):
        self.components.pop(component)
    
    def get(self,component):
        return self.components.get(component)


class Component:
    def __eq__(self,c):
        if type(self) == type(c):
            return self.__dict__ == c.__dict__
        
class System():
    '''
    Functions behind the components
    '''
    systems = []
    database = {}

    def __init__(self) -> None:
        self.entities = []
        if type(self) in System.database:
            raise Exception('Duplicate system types')
        System.systems.append(self)
        System.database[type(self)] = self

    def add_entity(self,entity):
        if entity not in self.entities:
            self.entities.append(entity)

    @classmethod
    def update_all(cls):
        for system in cls.systems:
            system.update()

    def update(self):
        pass
        
