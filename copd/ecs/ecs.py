class Entity:
    """
    Distinct Object
    """

    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def remove_component(self, component):
        self.components.pop(component)

    def get(self, component):
        return self.components.get(component)


class Component:
    def __eq__(self, c):
        if type(self) == type(c):
            return self.__dict__ == c.__dict__


class System:
    """
    Functions behind the components
    """

    def __init__(self):
        self.entities = []

    def add_entity(self, entity):
        if entity not in self.entities:
            self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def update(self):
        pass
