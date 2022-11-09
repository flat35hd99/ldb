import pandas as pd
from models.database import Database
from models.available_area import AvailableArea, BackGroundColor
from models.category import Category

class ServiceCollection():
    def __init__(self, database_df: pd.DataFrame, avalable_area_df: pd.DataFrame, category_df: pd.DataFrame, category_relation_df: pd.DataFrame) -> None:
        self.database_df = database_df
        self.available_area_df = avalable_area_df
        self.category_df = category_df
        self.category_relation_df = category_relation_df
    
    def get_all_databases_service(self):
        for row in self.database_df.itertuples(index=False):
            # Get AvailableArea
            # itertules() shoule return a single row
            area = self.get_available_area_by_id(row.available_area_id)
            
            simultaneous_connections = None
            if (row.simultaneous_connections):
                simultaneous_connections = row.simultaneous_connections
            
            d = Database(id = row.id, name = row.name, url = row.url, is_available_remote=row.is_available_remote, available_area=area, simultaneous_connections=simultaneous_connections)
            yield d
    
    def get_all_categories(self):
        for row in self.category_df.itertuples(index=False):
            c = Category(id = row.id, name = row.name)
            yield c

    def get_all_databases_by_category_id_service(self, category_id):
        for row in self.database_df.itertuples(index=False):
            # TODO: Impl
            pass
    
    def get_available_area_by_id(self, available_area_id):
        area_row = list(self.available_area_df[self.available_area_df.id == available_area_id].itertuples(index=False))[0]
        available_area = AvailableArea(id = available_area_id, name = area_row.name, background_color=BackGroundColor(area_row.background_color))
        return available_area

