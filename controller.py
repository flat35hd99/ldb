from views.table import CategoryTable, InitialTable
from service import ServiceCollection
from string import Template

class Controller:
    def __init__(self, service: ServiceCollection):
        self.service = service

    def create_category_html(self, lang="jp"):
        # カテゴリのリストを取得する
        categories = self.service.get_all_categories()

        created_html = ""

        # TODO: カテゴリのリストより上部の静的内容を追加する

        # カテゴリのリストを生成する
        created_html += '<div style="margin:10px 0;">'
        for c in categories:
            if lang == "jp":
                created_html += f'<span class="bullet3">▼</span><a href="#{c.html_id}">{c.name}</a>'
            elif lang == "en":
                created_html += f'<span class="bullet3">▼</span><a href="#{c.html_id}">{c.name_en}</a>'
            else:
                raise ValueError("lang must be 'jp' or 'en'")
        created_html += "</div>"

        # TODO: カテゴリのリスト以下のカラー例を追加する

        # カテゴリごとにデータベースのリストを取得し、HTMLに変換する
        # あらかじめ表示順にcategoriesをソートしておくことで、
        # 順番に生成されたHTMLを結合していく
        for c in categories:
            databases = self.service.get_all_databases_by_category_id_service(c.id)
            category_table = CategoryTable(category=c, databases=databases)
            created_html += category_table.str(lang=lang)

        # 全体のtemplateに流し込む
        # TODO: Viewに切り分ける必要あり。
        lang_dir = "" if lang == "jp" else "/en"
        with open(f"templates{lang_dir}/category.html", "r", encoding="utf8") as f:
            template = Template(f.read())
            whole_html = template.substitute({"tables": created_html})

        return whole_html

    def create_alphabet_html(self, lang="jp"):
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
            created_html += initial_table.str(lang=lang)

        # 全体のtemplateに流し込む
        # TODO: Viewに切り分ける必要あり。
        lang_dir = "" if lang == "jp" else "/en"
        with open(f"templates{lang_dir}/alphabet.html", "r", encoding="utf8") as f:
            template = Template(f.read())
            whole_html = template.substitute({"tables": created_html})

        return whole_html
