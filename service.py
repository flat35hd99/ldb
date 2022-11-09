import pandas as pd
from models.database import Database
from models.available_area import AvailableArea, BackGroundColor

class ServiceCollection():
    def __init__(self, database_df: pd.DataFrame, avalable_area_df: pd.DataFrame) -> None:
        self.database_df = database_df
        self.available_area_df = avalable_area_df
    
    def get_all_databases_service(self):
        for row in self.database_df.itertuples(index=False):
            # Get AvailableArea
            # itertules() shoule return a single row
            area_row = list(self.available_area_df[self.available_area_df.id == row.id].itertuples(index=False))[0]

            area = AvailableArea(id = row.available_area_id, name = area_row.name, background_color=BackGroundColor(area_row.background_color))
            
            simultaneous_connections = None
            if (row.simultaneous_connections):
                simultaneous_connections = row.simultaneous_connections
            
            d = Database(id = row.id, name = row.name, url = row.url, is_available_remote=row.is_available_remote, available_area=area, simultaneous_connections=simultaneous_connections)
            yield d
    
    