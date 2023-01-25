from models.category import Category
from models.database import Database
from string import Template

class CategoryTable():
    category_model: Category
    databases: list[Database]

    def __init__(self, category: Category, databases: list[Database]):
        self.category_model = category
        self.databases = databases

    def str(self):        
        # 各行のテンプレートをあらかじめメモリに読み込んでおく
        template_row = ""
        with open("templates/category_table_row.html", mode="r", encoding="utf8") as f:
            template_row = Template(f.read())
        
        rows = ""
        for d in self.databases:
            rows += template_row.substitute({
                "name": d.name,
                "url": d.url,
                "description": "d.description",
                "is_available_remote": d.text_is_available_remote(),
                "simultaneous_connections": d.text_simultaneous_connections(),
                "color": d.available_area.background_color,
                "available_area": d.available_area.name,
            })

        # TODO: 絶対パス、相対パスをいい感じに設定する
        with open("templates/category_table.html", mode="r", encoding="utf8") as f:
            template_table = Template(f.read())
            result = template_table.substitute({
                "category": self.category_model.name,
                "rows": rows
            })
            return result
