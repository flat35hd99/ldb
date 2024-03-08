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
        if database.name_note_en:
            template_obj["name_note"] = database.name_note_en
        if database.url_en:
            template_obj["url"] = database.url_en
        if database.available_area.name_en:
            template_obj["available_area"] = database.available_area.name_en
        if database.provider_en:
            template_obj["provider"] = database.provider_en
        if database.platform_en:
            template_obj["platform"] = database.platform_en
        if database.description_en:
            template_obj["description"] = database.description_en
        if database.simultaneous_connections_en:
            template_obj[
                "simultaneous_connections"
            ] = database.simultaneous_connections_en
        if database.note_en:
            template_obj["note"] = database.note_en
    else:
        raise ValueError(
            "プログラムのエラー: update_template_obj_with関数はlang='en'のときのみサポートしています。"
        )


def format_simultaneous_connections(simultaneous_connections, lang="jp"):
    if type(simultaneous_connections) == str:
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
    elif type(simultaneous_connections) == int:
        return str(simultaneous_connections)
    else:
        raise ValueError("simultaneous_connections must be int or str")


available_remote_mark = None
available_remote_mark_en = None


def format_available_remote(is_available_remote, lang="jp"):
    if not is_available_remote:
        return ""
    if lang == "jp":
        with open(
            "templates/available_remote_mark.html", mode="r", encoding="utf8"
        ) as f:
            global available_remote_mark
            available_remote_mark = f.read()
            return available_remote_mark
    elif lang == "en":
        with open(
            "templates/en/available_remote_mark.html", mode="r", encoding="utf8"
        ) as f:
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


def format_name_note(name_note, lang="jp"):
    if not name_note:
        return ""
    if lang == "jp":
        return f" ({name_note})"
    elif lang == "en":
        return f" ({name_note})"
    else:
        raise ValueError("lang must be 'jp' or 'en'")


# テンプレートに渡すオブジェクトを文字列へ変換する
def format_template_obj_with(template_obj, lang="jp"):
    template_obj["name_note"] = format_name_note(template_obj["name_note"], lang=lang)
    template_obj["simultaneous_connections"] = format_simultaneous_connections(
        template_obj["simultaneous_connections"], lang=lang
    )
    template_obj["available_remote"] = format_available_remote(
        template_obj["is_available_remote"], lang=lang
    )
    template_obj["provider"] = (
        f' ({template_obj["provider"]})' if template_obj["provider"] else ""
    )
    template_obj["platform"] = (
        f' [{template_obj["platform"]}]' if template_obj["platform"] else ""
    )
    template_obj["category"] = format_category(template_obj["category"], lang=lang)
    template_obj["note"] = template_obj["note"] if template_obj["note"] else ""
    template_obj["jp_only"] = "Ⓙ" if template_obj["jp_only"] else ""
    return template_obj


def get_name(database, lang="jp"):
    if lang == "jp":
        return database.name
    elif lang == "en":
        return database.name_en if database.name_en else database.name
    else:
        raise ValueError("lang must be 'jp' or 'en'")

def read_table_row_name(lang="jp"):
    if lang == "jp":
        with open(
            "templates/table_row_name.html", mode="r", encoding="utf8"
        ) as f:
            template_table_row_name = Template(f.read())
    elif lang == "en":
        with open(
            "templates/en/table_row_name.html", mode="r", encoding="utf8"
        ) as f:
            template_table_row_name = Template(f.read())
    return template_table_row_name

def read_table_row_name_element(lang="jp"):
    return Template('<a href="$url">$name</a>')

class CategoryTable:
    category_model: Category
    databases: Iterator[Database]

    def __init__(
        self,
        category: Category,
        databases: Iterator[Database],
    ):
        self.category_model = category
        self.databases = databases

    def str(self, lang="jp"):
        # 各行のテンプレートをあらかじめメモリに読み込んでおく
        template_row_name = read_table_row_name(lang=lang)
        template_row_name_element = read_table_row_name_element(lang=lang)
        template_row = ""
        if lang == "jp":
            with open(
                "templates/category_table_row.html", mode="r", encoding="utf8"
            ) as f:
                template_row = Template(f.read())

        elif lang == "en":
            with open(
                "templates/en/category_table_row.html", mode="r", encoding="utf8"
            ) as f:
                template_row = Template(f.read())
        else:
            raise ValueError("lang must be 'jp' or 'en'")

        rows = ""
        for d in self.databases:
            template_obj = {
                "name": get_name(database=d, lang=lang),
                "name_note": d.name_note,
                "provider": d.provider,
                "platform": d.platform,
                "url": d.url,
                "description": d.description,
                "is_available_remote": d.is_available_remote,
                "simultaneous_connections": d.simultaneous_connections,
                "color": d.text_background_color(),
                "available_area": d.available_area.name,
                "category": [],  # 不要
                "note": d.note,
                "jp_only": d.jp_only,
            }

            if lang == "en":
                update_template_obj_with(template_obj, d, lang=lang)
            
            template_obj = format_template_obj_with(template_obj, lang=lang)
            if template_obj["url"]:
                template_obj["name_element"] = template_row_name_element.substitute(template_obj)
            else:
                template_obj["name_element"] = template_obj["name"]
            template_obj["name_line"] = template_row_name.substitute(template_obj)

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
            with open(
                "templates/en/category_table.html", mode="r", encoding="utf8"
            ) as f:
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


class InitialRows:
    initial_char: str
    databases: Iterator[Database]

    def __init__(self, initial_char: str, databases: Iterator[Database]):
        self.initial_char = initial_char.upper()
        self.databases = databases

    def str(self, lang="jp"):
        # 各行のテンプレートをあらかじめメモリに読み込んでおく
        template_row_name = read_table_row_name(lang=lang)
        template_row_name_element = read_table_row_name_element(lang=lang)
        template_row = ""
        if lang == "jp":
            with open(
                "templates/alphabet_table_row.html", mode="r", encoding="utf8"
            ) as f:
                template_row = Template(f.read())
        elif lang == "en":
            with open(
                "templates/en/alphabet_table_row.html", mode="r", encoding="utf8"
            ) as f:
                template_row = Template(f.read())
        else:
            raise ValueError("lang must be 'jp' or 'en'")

        rows = ""
        is_first = True  # 最初の行だけアルファベットを表示させるためのフラグ
        for d in self.databases:
            initial_element = (
                f'<th rowspan="{len(self.databases)}" id="db{self.initial_char}">{self.initial_char}</th>'
                if is_first
                else ""
            )
            is_first = False

            # はじめに日本語をデフォルトとして設定し、存在するときだけ英語を設定する
            template_obj = {
                "initial": initial_element,
                "name": get_name(database=d, lang=lang),
                "name_note": d.name_note,
                "provider": d.provider,
                "platform": d.platform,
                "url": d.url,
                "description": d.description,
                "is_available_remote": d.is_available_remote,
                "simultaneous_connections": d.simultaneous_connections,
                "color": d.text_background_color(),
                "available_area": d.available_area.name,
                "category": self.filter_categories(d.categories),
                "note": d.note,
                "jp_only": d.jp_only,
            }

            if lang == "en":
                update_template_obj_with(template_obj, d, lang=lang)

            template_obj = format_template_obj_with(template_obj, lang=lang)
            if template_obj["url"]:
                template_obj["name_element"] = template_row_name_element.substitute(template_obj)
            else:
                template_obj["name_element"] = template_obj["name"]
            template_obj["name_line"] = template_row_name.substitute(template_obj)
            
            rows += template_row.substitute(template_obj)

            if is_first:
                is_first = False

        return rows

    def filter_categories(self, categories: list[Category]):
        # アルファベット表示における総合分野、総合分野(国内）、総合分野（国外）
        # と社会科学、人文科学、自然科学、生命科学に関する取扱い
        # sougou_idsに含まれるカテゴリがカテゴリの中にあるとき、
        # shizen_seimei_jinbun_syakai_idsのカテゴリを除去する
        sougou_ids = {1, 17, 18}
        shizen_seimei_jinbun_syakai_ids = {3, 4, 15, 16}

        category_ids = set([c.id for c in categories])
        if sougou_ids not in category_ids:
            # カテゴリに総合分野が含まれていないときは、そのまま
            return categories
        else:
            # カテゴリに総合分野を含むときは、{自然科学、生命科学、人文科学、社会科学}を除外する
            ids = category_ids - shizen_seimei_jinbun_syakai_ids
            return [c for c in categories if c.id in ids]
