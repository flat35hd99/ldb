from enum import Enum


class BackGroundColor(Enum):
    green = "green"
    yellow = "yellow"
    red = "red"


class AvailableArea:
    def __init__(self, id, name, name_en, background_color: BackGroundColor) -> None:
        self.id = id
        self.name = name
        self.name_en = name_en
        self.background_color = background_color
