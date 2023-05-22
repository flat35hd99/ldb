import pandas as pd
from models.database import Database
from models.available_area import AvailableArea, BackGroundColor
from models.category import Category
from collections.abc import Iterator
import functools


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
        self.database_df = database_df
        self.available_area_df = avalable_area_df
        self.category_df = category_df
        self.categories = None

    def get_all_databases_service(self) -> Iterator[Database]:
        for row in self.database_df.itertuples(index=False):
            # Get AvailableArea
            # itertules() shoule return a single row
            area = self.get_available_area_by_id(row.available_area_id)

            simultaneous_connections = None
            if row.simultaneous_connections:
                simultaneous_connections = row.simultaneous_connections

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

            d = Database(
                id=row.id,
                name=row.name,
                name_en=row.name_en,
                url=row.url,
                is_available_remote=row.is_available_remote,
                available_area=area,
                simultaneous_connections=simultaneous_connections,
                description=row.description,
                description_en=row.description_en,
                initial_char=row.initial,
                second_char=row.second_char,
                third_char=row.third_char,
                categories=categories,
            )
            yield d

    def get_all_categories(self) -> Iterator[Category]:
        if self.categories:
            return self.categories

        categories = []
        for row in self.category_df.itertuples(index=False):
            categories.append(Category(id=row.id, name=row.name, html_id=row.html_id))

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
            simultaneous_connections = None
            if row.simultaneous_connections:
                simultaneous_connections = row.simultaneous_connections

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

            d = Database(
                id=row.id,
                name=row.name,
                name_en=row.name_en,
                url=row.url,
                is_available_remote=row.is_available_remote,
                available_area=area,
                simultaneous_connections=simultaneous_connections,
                description=row.description,
                description_en=row.description_en,
                initial_char=row.initial,
                second_char=row.second_char,
                third_char=row.third_char,
                categories=categories,
            )
            yield d

    def get_available_area_by_id(self, available_area_id):
        area_row = list(
            self.available_area_df[
                self.available_area_df.id == available_area_id
            ].itertuples(index=False)
        )[0]

        id = available_area_id
        name = area_row.name
        bg = BackGroundColor(area_row.background_color)

        available_area = AvailableArea(id=id, name=name, background_color=bg)
        return available_area

    def get_all_initials(self) -> Iterator[str]:
        return list(self.database_df.initial.unique())

    def get_all_databases_by_initial(self, initial_char: str) -> Iterator[Database]:
        result = []
        for d in self.get_all_databases_service():
            if d.initial_char == initial_char:
                result.append(d)

        # Sort by second and third character
        # aとbで、aがはじめの方なら-1, aが後ろの方なら+1, 同じなら0。
        def compare_initial(a: Database, b: Database):
            if a.second_char < b.second_char:
                return -1
            elif a.second_char > b.second_char:
                return 1
            else:
                if a.third_char < b.third_char:
                    return -1
                elif a.third_char > b.third_char:
                    return 1
                else:
                    return 0

        result = sorted(result, key=functools.cmp_to_key(compare_initial))

        return result
