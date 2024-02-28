import math
import pandas as pd

class Database:
    def __init__(
        self,
        id,
        name,
        name_en,
        url,
        is_available_remote,
        available_area,
        simultaneous_connections,
        description,
        description_en,
        initial_char,
        categories,
    ) -> None:
        self.id = id
        self.name = name
        if pd.isna(name_en):
            self.name_en = None
        else:
            self.name_en = name_en
        self.url = url
        self.is_available_remote = is_available_remote
        self.available_area = available_area
        self.simultaneous_connections = simultaneous_connections
        self.description = description
        if pd.isna(description_en):
            self.description_en = None
        else:
            self.description_en = description_en
        self.initial_char = initial_char
        self.cateogries = categories

    def text_is_available_remote(self):
        return "R" if self.is_available_remote else "no"

    def text_simultaneous_connections(self):
        if (
            self.simultaneous_connections == 0
            or self.simultaneous_connections == None
            or math.isnan(self.simultaneous_connections)
        ):
            return ""
        elif self.simultaneous_connections == -1:
            return "無制限"
        else:
            return self.simultaneous_connections

    def text_background_color(self):
        aa = self.available_area
        return aa.background_color.name

    def text_categories(self):
        return ", ".join([c.name for c in self.cateogries])


class DatabaseFactory:
    def create():
        pass
