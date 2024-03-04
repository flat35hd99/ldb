import pandas as pd
from models.database import Database
from models.available_area import AvailableArea, BackGroundColor
from models.category import Category
from models.literature_language import LiteratureLanguage
from collections.abc import Iterator

def factory_database(row, area, categories, literature_languages):
    d = Database(
        id=row.id,
        name=row.name,
        name_en=row.name_en,
        url=row.url,
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
        literature_languages=literature_languages,
    )
    return d

class ServiceCollection:
    database_df: pd.DataFrame
    available_area_df: pd.DataFrame
    category_df: pd.DataFrame
    literature_language_df: pd.DataFrame
    categories: Iterator[Category]

    def __init__(
        self,
        database_df: pd.DataFrame,
        avalable_area_df: pd.DataFrame,
        category_df: pd.DataFrame,
        literature_language_df: pd.DataFrame,
    ) -> None:
        self.database_df = database_df
        self.available_area_df = avalable_area_df
        self.category_df = category_df
        self.literature_language_df = literature_language_df
        self.categories = None

    def get_all_databases_service(self) -> Iterator[Database]:
        for row in self.database_df.itertuples(index=False):
            # Get AvailableArea
            # itertules() shoule return a single row
            area = self.get_available_area_by_id(row.available_area_id)

            # Get category
            # A Database belongs to one or more categories
            all_categories = self.get_all_categories()
            categories = []
            if type(row.category_id) == int:
                for c in all_categories:
                    if c.id == row.category_id:
                        categories.append(c)
            else:
                for category_id in row.category_id:
                    # Find category from categories
                    for c in all_categories:
                        if c.id == category_id:
                            categories.append(c)

            # Get literature languages
            literature_languages = self.get_literature_languages_by_id(row.literature_language_id)

            d = factory_database(row, area, categories, literature_languages)
            yield d

    def get_all_categories(self) -> Iterator[Category]:
        if self.categories:
            return self.categories

        categories = []
        for row in self.category_df.itertuples(index=False):
            categories.append(Category(id=row.id, name=row.name, name_en=row.name_en, html_id=row.html_id))

        self.categories = categories

        return categories

    def get_all_databases_by_category_id_service(
        self, category_id
    ) -> Iterator[Database]:
        for c in self.get_all_categories():
            if c.id == category_id:
                category = c
                break
        try:
            category
        except NameError:
            raise ValueError("Category not found")

        db_df = self.database_df[self.database_df.category_id == category_id]

        for row in db_df.itertuples(index=False):
            area = self.get_available_area_by_id(row.available_area_id)

            # Get category
            # A Database belongs to one or more categories
            all_categories = self.get_all_categories()
            categories = []
            if type(row.category_id) == int:
                for c in all_categories:
                    if c.id == row.category_id:
                        categories.append(c)
                        break
            else:
                for category_id in row.category_id:
                    # Find category from categories
                    for c in all_categories:
                        if c.id == category_id:
                            categories.append(c)
                            break

            # Get literature languages
            literature_languages = self.get_literature_languages_by_id(row.literature_language_id)

            d = factory_database(row, area, categories, literature_languages)
            yield d

    def get_available_area_by_id(self, available_area_id):
        try:
            area_row = list(
                self.available_area_df[
                    self.available_area_df.id == available_area_id
                ].itertuples(index=False)
            )[0]
        except IndexError:
            raise ValueError(f"avairable_area_id {available_area_id}が見つかりません。databaseの表とavailable_areaの表が正しく紐づいているか確認してください。")

        id = available_area_id
        name = area_row.name
        name_en = area_row.name_en
        bg = BackGroundColor(area_row.background_color)

        available_area = AvailableArea(id=id, name=name, name_en=name_en, background_color=bg)
        return available_area

    def get_literature_languages_by_id(self, literature_language_id):
        try:
            language_rows = list(
                self.literature_language_df[
                    self.literature_language_df.id == literature_language_id
                ].itertuples(index=False)
            )
        except IndexError:
            raise ValueError(f"literature_language_id {literature_language_id}が見つかりません。databaseの表とliterature_languageの表が正しく紐づいているか確認してください。")

        return [
            LiteratureLanguage(
                id=row.id, name=row.name, name_en=row.name_en
            )
            for row in language_rows
        ]

    def get_all_initials(self) -> Iterator[str]:
        return list(self.database_df.initial.unique())

    def get_all_databases_by_initial(self, initial_char: str) -> Iterator[Database]:
        result = []
        for d in self.get_all_databases_service():
            if d.initial_char == initial_char:
                result.append(d)

        return result
