class Database():
    def __init__(self, id, name, url, is_available_remote, available_area, simultaneous_connections) -> None:
        self.id = id
        self.name = name
        self.url = url
        self.is_available_remote = is_available_remote
        self.available_area = available_area
        self.simultaneous_connections = simultaneous_connections

class DatabaseFactory():
    def create():
        pass