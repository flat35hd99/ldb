from views.table import CategoryTable, InitialTable
from service import ServiceCollection

class Controller():
    def __init__(self, service: ServiceCollection):
        self.service = service
    
    def create_category_html(self, lang = "ja"):
        # カテゴリのリストを取得する
        categories = self.service.get_all_categories()

        created_html = ""
        
        # TODO: カテゴリのリストより上部の静的内容を追加する
        
        # カテゴリのリストを生成する
        created_html += "<div style=\"margin:10px 0;\">"
        for c in categories:
            created_html += f"<span class=\"bullet3\">▼</span><a href=\"#{c.html_id}\">{c.name}</a>"
        created_html += "</div>"
        
        # TODO: カテゴリのリスト以下のカラー例を追加する

        # カテゴリごとにデータベースのリストを取得し、HTMLに変換する
        # あらかじめ表示順にcategoriesをソートしておくことで、
        # 順番に生成されたHTMLを結合していく
        for c in categories:
            databases = self.service.get_all_databases_by_category_id_service(c.id)
            category_table = CategoryTable(category=c, databases=databases)
            created_html += category_table.str()
        
        return created_html

    def create_alphabet_html(self, lang = "ja"):
        # 先頭文字のリストを取得する
        initials = self.service.get_all_initials()
        
        created_html = ""
        
        # TODO: テーブルより上部の静的内容を追加する
        # TODO: 頭文字のリストを追加する
        
        # 先頭文字ごとにデータベースのリストを取得し、HTMLに変換する
        # あらかじめ表示順にinitialsをソートしておくことで、
        # 順番に生成されたHTMLを結合していく
        for initial_char in initials:
            databases = self.service.get_all_databases_by_initial(initial_char)
            initial_table = InitialTable(initial_char=initial_char, databases=databases)
            created_html += initial_table.str()
