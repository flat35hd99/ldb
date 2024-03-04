import math
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
        if database.available_area.name_en:
            template_obj["available_area"] = database.available_area.name_en
        if database.provider_en:
            template_obj["provider"] = database.provider_en
        if database.platform_en:
            template_obj["platform"] = database.platform_en
        if database.description_en:
            template_obj["description"] = database.description_en
        if database.simultaneous_connections_en:
            template_obj["simultaneous_connections"] = database.simultaneous_connections_en
        if database.note_en:
            template_obj["note"] = database.note_en
    else:
        raise ValueError("プログラムのエラー: update_template_obj_with関数はlang='en'のときのみサポートしています。")

def format_simultaneous_connections(simultaneous_connections, lang="jp"):
        if(type(simultaneous_connections) == str):
            return simultaneous_connections
        if (
            simultaneous_connections == 0
            or simultaneous_connections == None
            or math.isnan(simultaneous_connections)
        ):
            return ""
        elif simultaneous_connections == -1:
            if lang == "jp":
                return "無制限"
            elif lang == "en":
                return "Unlimited"
            else:
                raise ValueError("lang must be 'jp' or 'en'")
        elif(type(simultaneous_connections) == int):
            return str(simultaneous_connections)
        else:
            raise ValueError("simultaneous_connections must be int or str")

available_remote_mark = None
available_remote_mark_en = None
def format_available_remote(is_available_remote, lang="jp"):
    if not is_available_remote:
        return ""
    if lang == "jp":
        with open("templates/available_remote_mark.html", mode="r", encoding="utf8") as f:
            global available_remote_mark
            available_remote_mark = f.read()
            return available_remote_mark
    elif lang == "en":
        with open("templates/en/available_remote_mark.html", mode="r", encoding="utf8") as f:
            global available_remote_mark_en
            available_remote_mark_en = f.read()
            return available_remote_mark_en
    else:
        raise ValueError("lang must be 'jp' or 'en'")

def format_category(categories, lang="jp"):
    if lang == "jp":
        category_template = Template('<a href="index.html#$html_id">$name</a>')
    elif lang == "en":
        category_template = Template('<a href="index_e.html#$html_id">$name_en</a>')
    else:
        raise ValueError("lang must be 'jp' or 'en'")
    
    return "<br>".join(
        [
            category_template.substitute(
                {"html_id": c.html_id, "name": c.name, "name_en": c.name_en}
            )
            for c in categories
        ]
    )

def format_template_obj_with(template_obj, lang="jp"):
    template_obj["simultaneous_connections"] = format_simultaneous_connections(template_obj["simultaneous_connections"], lang=lang)
    template_obj["available_remote"] = format_available_remote(template_obj["is_available_remote"], lang=lang)
    template_obj["provider"] = f' ({template_obj["provider"]})' if template_obj["provider"] else ""
    template_obj["platform"] = f' [{template_obj["platform"]}]' if template_obj["platform"] else ""
    template_obj["category"] = format_category(template_obj["category"], lang=lang)
    template_obj["note"] = template_obj["note"] if template_obj["note"] else ""
    return template_obj

def get_name(database, lang="jp"):
    if lang == "jp":
        return database.name
    elif lang == "en":
        return database.name_en
    else:
        raise ValueError("lang must be 'jp' or 'en'")

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
                "provider": d.provider,
                "platform": d.platform,
                "url": d.url,
                "description": d.description,
                "is_available_remote": d.is_available_remote,
                "simultaneous_connections": d.simultaneous_connections,
                "color": d.text_background_color(),
                "available_area": d.available_area.name,
                "category": [], # 不要
                "note": d.note,
            }
            
            if lang == "en":
                update_template_obj_with(template_obj, d, lang=lang)

            template_obj = format_template_obj_with(template_obj, lang=lang)

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
                "provider": d.provider,
                "platform": d.platform,
                "url": d.url,
                "description": d.description,
                "is_available_remote": d.is_available_remote,
                "simultaneous_connections": d.simultaneous_connections,
                "color": d.text_background_color(),
                "available_area": d.available_area.name,
                "category": d.categories,
                "note": d.note,
            }

            if lang == "en":
                update_template_obj_with(template_obj, d, lang=lang)

            template_obj = format_template_obj_with(template_obj, lang=lang)
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
