import abc
from string import Template

class IComposition(metaclass=abc.ABCMeta):
    def to_html(self, filename) -> None:
        with open(filename, "rw") as f:
            f.write(self.build())

    @abc.abstractmethod
    def build(self) -> str:
        raise NotImplementedError()

class Row(IComposition):
    def __init__(self, template: Template) -> None:
        self.template = template
    
    def build(self) -> str:
        return self.template.substitute(
            
        )
