from string import Template


class Controller():
    def __init__(self, service):
        self.service = service
    
    def create_category_html(self, lang = "ja"):
        raise NotImplementedError()