import pytest
from controller import Controller
from service import ServiceCollection
import pandas as pd

def new_service_collection():
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
    }), category_df=pd.DataFrame(data={
        'id': [1],
        'name': ['社会科学']
    }), category_relation_df=pd.DataFrame(data={
        'database_id': [1],
        'category_id': [1]
    }))
    return service

def test_controller_initilization():
    s = new_service_collection()
    c = Controller(service = s)
    assert c is not None

def test_controller_create_category_html():
    s = new_service_collection()
    c = Controller(service = s)
    html = c.create_category_html()
    assert type(html) == str
    assert len(html) > 0
