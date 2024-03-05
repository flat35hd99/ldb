class Category:
    def __init__(self, id, name, name_en, html_id) -> None:
        self.id = id
        self.name = name
        self.name_en = name_en
        self.html_id = html_id
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Category):
            return self.id == other.id
        return False