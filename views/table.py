from models.category import Category
from models.database import Database
from string import Template
from collections.abc import Iterator

# 外国語向けに、テンプレートに渡すオブジェクトを更新する
# 注意: template_objはミュータブル
def update_template_obj_with(template_obj, database, lang="en"):
    if lang == "en":
        if database.name_en:
            template_obj["name"] = database.name_en
        if database.description_en:
            template_obj["description"] = database.description_en
    else:
        raise ValueError("update_template_obj_with() lang must be 'en'")

def get_name(database, lang="jp"):
    if lang == "jp" and database.provider is not None:
        return f"{database.name}({database.provider})"
    elif lang == "en" and database.provider is not None:
        return f"{database.name_en}({database.provider_en})"
    elif lang == "jp":
        return database.name
    elif lang == "en":
        return database.name_en

class CategoryTable:
    category_model: Category
    databases: Iterator[Database]

    def __init__(self, category: Category, databases: Iterator[Database]):
        self.category_model = category
        self.databases = databases

    def str(self, lang="jp"):
        # 各行のテンプレートをあらかじめメモリに読み込んでおく
        template_row = ""
        if lang == "jp":
            with open("templates/category_table_row.html", mode="r", encoding="utf8") as f:
                template_row = Template(f.read())
        elif lang == "en":
            with open("templates/en/category_table_row.html", mode="r", encoding="utf8") as f:
                template_row = Template(f.read())
        else:
            raise ValueError("lang must be 'jp' or 'en'")

        rows = ""
        for d in self.databases:
            template_obj = {
                "name": get_name(database=d, lang=lang),
                "url": d.url,
                "description": d.description,
                "is_available_remote": d.text_is_available_remote(),
                "simultaneous_connections": d.text_simultaneous_connections(),
                "color": d.text_background_color(),
                "available_area": d.available_area.name,
            }
            
            if lang == "en":
                update_template_obj_with(template_obj, d, lang=lang)

            rows += template_row.substitute(template_obj)

        if lang == "jp":
            with open("templates/category_table.html", mode="r", encoding="utf8") as f:
                template_table = Template(f.read())
                result = template_table.substitute(
                    {
                        "category": self.category_model.name,
                        "html_id": self.category_model.html_id,
                        "rows": rows,
                    }
                )
                return result
        elif lang == "en":
            with open("templates/en/category_table.html", mode="r", encoding="utf8") as f:
                template_table = Template(f.read())
                result = template_table.substitute(
                    {
                        "category": self.category_model.name_en,
                        "html_id": self.category_model.html_id,
                        "rows": rows,
                    }
                )
                return result
        else:
            raise ValueError("lang must be 'jp' or 'en'")


class InitialTable:
    initial_char: str
    databases: Iterator[Database]

    def __init__(self, initial_char: str, databases: Iterator[Database]):
        self.initial_char = initial_char.upper()
        self.databases = databases

    def str(self, lang="jp"):
        # 各行のテンプレートをあらかじめメモリに読み込んでおく
        template_row = ""
        if lang == "jp":
            with open("templates/alphabet_table_row.html", mode="r", encoding="utf8") as f:
                template_row = Template(f.read())
        elif lang == "en":
            with open("templates/en/alphabet_table_row.html", mode="r", encoding="utf8") as f:
                template_row = Template(f.read())
        else:
            raise ValueError("lang must be 'jp' or 'en'")

        rows = ""
        is_first = True # 最初の行だけアルファベットを表示させるためのフラグ
        for d in self.databases:
            initial_element = f'<th rowspan="{len(self.databases)}">{self.initial_char}</th>' if is_first else ""
            is_first = False
            
            # はじめに日本語をデフォルトとして設定し、存在するときだけ英語を設定する
            template_obj = {
                "initial": initial_element,
                "name": get_name(database=d, lang=lang),
                "url": d.url,
                "description": d.description,
                "is_available_remote": d.text_is_available_remote(),
                "simultaneous_connections": d.text_simultaneous_connections(),
                "color": d.text_background_color(),
                "available_area": d.available_area.name,
                "category": d.text_categories(),
            }

            if lang == "en":
                update_template_obj_with(template_obj, d, lang=lang)

            rows += template_row.substitute(template_obj)
            
            if is_first:
                is_first = False

        if lang == "jp":
            with open("templates/alphabet_table.html", mode="r", encoding="utf8") as f:
                template_table = Template(f.read())
                result = template_table.substitute({"rows": rows})
                return result
        elif lang == "en":
            with open("templates/en/alphabet_table.html", mode="r", encoding="utf8") as f:
                template_table = Template(f.read())
                result = template_table.substitute({"rows": rows})
                return result
