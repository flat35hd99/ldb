from views.category_table import CategoryTable
from service import ServiceCollection

class Controller():
    def __init__(self, service: ServiceCollection):
        self.service = service
    
    def create_category_html(self, lang = "ja"):
        # カテゴリのリストを取得する
        categories = self.service.get_all_categories()

        # カテゴリごとにデータベースのリストを取得し、HTMLに変換する
        # あらかじめ表示順にcategoriesをソートしておくことで、
        # 順番に生成されたHTMLを結合していく
        created_html = ""
        for c in categories:
            databases = self.service.get_all_databases_by_category_id_service(c.id)
            category_table = CategoryTable(category=c, databases=databases)
            created_html += category_table.str()
        
        return created_html
