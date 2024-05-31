from enum import Enum


class OPTIONS(Enum):
    CAPTION = 1
    PRINT = 2
    HANDLER = 3


class Option:
    def __init__(self, type, data):
        self.type = type
        self.data = data


# TODO: Replace handler code in menus.Menu with an event handler class.
class EventHandler:
    def __init__(self):
        pass
