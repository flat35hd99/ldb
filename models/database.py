class Database():
    def __init__(self, id, name, url, is_available_remote, available_area, simultaneous_connections) -> None:
        self.id = id
        self.name = name
        self.url = url
        self.is_available_remote = is_available_remote
        self.available_area = available_area
        self.simultaneous_connections = simultaneous_connections
    
    def text_is_available_remote(self):
        return "yes" if self.is_available_remote else "no"

    def text_simultaneous_connections(self):
        if self.simultaneous_connections == 0 or self.simultaneous_connections == None:
            return ""
        elif self.simultaneous_connections == -1:
            return "無制限"
        else:
            return self.simultaneous_connections

class DatabaseFactory():
    def create():
        pass