from enum import Enum

class BackGroundColor(Enum):
    GREEN = 1
    YELLOW = 2
    RED = 3

class AvailableArea():
    def __init__(self, id, name, background_color: BackGroundColor) -> None:
        self.id = id
        self.name = name
        self.background_color = background_color
