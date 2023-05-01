from ..views.table import CategoryTable
from ..service import ServiceCollection

from .test_service import new_service_collection

def test_one_category_table():
    s = new_service_collection()
    
    categories = s.get_all_categories()
    c = next(categories) # 最初のカテゴリだけでテスト
    databases = s.get_all_databases_by_category_id_service(category_id=c.id)
    
    view = CategoryTable(category=c, databases=databases)
    result = view.str()
    assert type(result) == str
    assert result != ""

def test_multiple_tables():
    s = new_service_collection()
    categories = s.get_all_categories()
    
    result = ""
    for c in categories:
        databases = s.get_all_databases_by_category_id_service(category_id=c.id)
        
        view = CategoryTable(category=c, databases=databases)
        result += view.str()

    assert type(result) == str
    assert result != ""
