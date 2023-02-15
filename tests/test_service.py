import pandas as pd
from ..service import ServiceCollection
from ..models.database import Database
from ..models.available_area import BackGroundColor

def new_service_collection():
    """Create new ServiceCollection instance for testing

    Returns:
        ServiceCollection: ServiceCollection instance
    """
    service = ServiceCollection(database_df=pd.DataFrame(data = {
        'id': [1],
        'name': ['exampleDB'],
        'url': ['https://example.com'],
        'is_available_remote': [True],
        'available_area_id': [1],
        'simultaneous_connections': [None],
        'category_id': [4],
    }), avalable_area_df=pd.DataFrame(data={
        'id': [1],
        'name': ['学内'],
        'background_color': 'green'
    }), category_df=pd.DataFrame(data={
        'id': [4],
        'name': ['社会科学']
    }))
    return service

def test_get_all_databases_service():
    # Initilize
    service = new_service_collection()
    
    dbs = service.get_all_databases_service() # Check if the call does not cause error implicitly
    assert dbs is not None

    db = list(dbs)[0]
    assert db.available_area.id is 1
    assert db.available_area.name is '学内'
    assert db.available_area.background_color.value is BackGroundColor.green.value

def test_get_all_categories():
    service = new_service_collection()

    categories = service.get_all_categories()
    assert categories is not None

def test_get_all_databases_by_category_id_service():
    service = new_service_collection()
    categories = service.get_all_categories()
    c = list(categories)[0]
    
    dbs = service.get_all_databases_by_category_id_service(category_id=c.id)
    assert dbs is not None
