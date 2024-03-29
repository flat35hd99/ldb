from .. import defined_types
import pandas as pd


def get_categories_by_DBID(category_df: pd.DataFrame, database_id: defined_types.ID):
    category_rows = category_df[category_df["database_id"] == database_id]
