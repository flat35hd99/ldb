import pandas as pd
from models.database import Database
from models.available_area import AvailableArea, BackGroundColor
from models.category import Category
from collections.abc import Iterator


def factory_database(row, area, categories):
    d = Database(
        id=row.id,
        name=row.name,
        name_en=row.name_en,
        name_note=row.name_note,
        name_note_en=row.name_note_en,
        url=row.url,
        url_en=row.url_en,
        is_available_remote=row.is_available_remote,
        available_area=area,
        simultaneous_connections=row.simultaneous_connections,
        simultaneous_connections_en=row.simultaneous_connections_en,
        description=row.description,
        description_en=row.description_en,
        initial_char=row.initial,
        categories=categories,
        provider=row.provider,
        provider_en=row.provider_en,
        platform=row.platform,
        platform_en=row.platform_en,
        note=row.note,
        note_en=row.note_en,
        jp_only=row.jp_only,
    )
    return d


class ServiceCollection:
    database_df: pd.DataFrame
    available_area_df: pd.DataFrame
    category_df: pd.DataFrame
    categories: Iterator[Category]

    def __init__(
        self,
        database_df: pd.DataFrame,
        avalable_area_df: pd.DataFrame,
        category_df: pd.DataFrame,
    ) -> None:
        # databaseの初期化前にavailable_areaとcategoryを初期化する必要がある
        self.available_area_df = avalable_area_df
        self.available_areas = None
        
        self.category_df = category_df
        self.categories = []
        for row in self.category_df.itertuples(index=False):
            self.categories.append(
                Category(
                    id=row.id, name=row.name, name_en=row.name_en, html_id=row.html_id
                )
            )
            
        self.database_df = database_df
        self.databases = []
        for row in self.database_df.itertuples(index=False):
            # Get AvailableArea
            area = self.get_available_area_by_id(row.available_area_id)

            # Get category
            # A Database belongs to one or more categories
            all_categories = self.categories
            categories = []
            if type(row.category_id) == int:
                for c in all_categories:
                    if c.id == row.category_id:
                        categories.append(c)
            else:
                # category_idに複数のカテゴリが入っている場合
                try:
                    for category_id in [int(x) for x in row.category_id.split(",")]:
                        # Find category from categories
                        for c in all_categories:
                            if c.id == category_id:
                                categories.append(c)
                except AttributeError:
                    raise ValueError(f"database_id: {row.id}のcategory_idが不正な値です。カテゴリのidは,(カンマ)区切りです。")

            d = factory_database(row, area, categories)
            self.databases.append(d)

    # 有効なカテゴリのみを取得する
    def get_all_categories(self) -> Iterator[Category]:
        return [c for c in self.categories if len(self.get_all_databases_by_category_id_service(c.id)) > 0]

    def get_all_databases_by_category_id_service(
        self, category_id
    ) -> Iterator[Database]:
        for c in self.categories:
            if c.id == category_id:
                category = c
                break
        try:
            category
        except NameError:
            raise ValueError("Category not found")

        filtered_databases = []
        for d in self.databases:
            if category in d.categories:
                filtered_databases.append(d)

        return filtered_databases

    def get_available_area_by_id(self, available_area_id):
        try:
            area_row = list(
                self.available_area_df[
                    self.available_area_df.id == available_area_id
                ].itertuples(index=False)
            )[0]
        except IndexError:
            raise ValueError(
                f"avairable_area_id {available_area_id}が見つかりません。databaseの表とavailable_areaの表が正しく紐づいているか確認してください。"
            )

        id = available_area_id
        name = area_row.name
        name_en = area_row.name_en
        bg = BackGroundColor(area_row.background_color)

        available_area = AvailableArea(
            id=id, name=name, name_en=name_en, background_color=bg
        )
        return available_area

    def get_all_initials(self) -> Iterator[str]:
        return [str(s) for s in list(self.database_df.initial.unique())]

    def get_all_databases_by_initial(self, initial_char: str) -> Iterator[Database]:
        result = []
        for d in self.databases:
            if d.initial_char == initial_char:
                result.append(d)

        return result
