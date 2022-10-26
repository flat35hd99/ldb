from .. import types
import pandas as pd

def get_categories_by_DBID(category_df: pd.DataFrame, database_id: types.ID):
    category_rows =  category_df[category_df["database_id"] == database_id]

    