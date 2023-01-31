from controller import Controller
from .test_service import new_service_collection

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
