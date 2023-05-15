import math


class Database:
    def __init__(
        self,
        id,
        name,
        url,
        is_available_remote,
        available_area,
        simultaneous_connections,
        description,
        initial_char,
        second_char,
        third_char,
        categories,
    ) -> None:
        self.id = id
        self.name = name
        self.url = url
        self.is_available_remote = is_available_remote
        self.available_area = available_area
        self.simultaneous_connections = simultaneous_connections
        self.description = description
        self.initial_char = initial_char
        self.second_char = second_char
        self.third_char = third_char
        self.cateogries = categories

    def text_is_available_remote(self):
        return "yes" if self.is_available_remote else "no"

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
