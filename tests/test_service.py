from typing import Generator
import pandas as pd
from ..service import ServiceCollection
from ..models.database import Database
from ..models.available_area import BackGroundColor

def test_get_all_databases_service():
    # Initilize
    service = ServiceCollection(database_df=pd.DataFrame(data = {
        'id': [1],
        'name': ['exampleDB'],
        'url': ['https://example.com'],
        'is_available_remote': [True],
        'available_area_id': [1],
        'simultaneous_connections': [None]
    }), avalable_area_df=pd.DataFrame(data={
        'id': [1],
        'name': ['学内'],
        'background_color': 1
    }))
    
    dbs = service.get_all_databases_service() # Check if the call does not cause error implicitly
    assert dbs is not None
    assert isinstance(dbs, Generator)

    db = list(dbs)[0]
    assert db.available_area.id is 1
    assert db.available_area.name is '学内'
    assert db.available_area.background_color.value is BackGroundColor.GREEN.value
    