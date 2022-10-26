import pandas as pd

class Category(Enum):
    sougou = 1
    science_technology_machanics = 2
    humanities = 3
    social_science = 4
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def get_name(self):
        return self.name

def new_categories(df: pd.Dataframe):
    return 1
