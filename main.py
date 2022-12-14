from string import Template
import pandas as pd
from service import ServiceCollection

def create_category_html():
    output_filepath = ""
    
    with open("templates/category_table.html", encoding="utf8") as f:
        category_table = Template(f.read())
    with open("templates/category_row.html", encoding="utf8") as f:
        category_row = Template(f.read())
    with open("templates/available_remote_mark.html", encoding="utf8") as f:
        available_remote_mark = f.read()

    dfs = pd.read_excel("master.xlsx", sheet_name=["database", "category", "category_relation", "available_area"])
    database_df = dfs["database"]
    category_df = dfs["category"]
    category_relation_df = dfs["category_relation"]
    available_area_df = dfs["available_area"]
    
    service = ServiceCollection(database_df, available_area_df, category_df, category_relation_df)
    # controller = Controller(service)
    # controller.create_category_html()
    # controller.create_alphabet_html()

def create_alphabet_html():
    pass

# (Category instance, database_df)のsetの配列を返す
# [
#   (Category, pandas.Dataframe),
# ]
def divide_into_category(database_df, category_df, category_relation_df):
    pass

if __name__ == '__main__':
    create_category_html()
    create_alphabet_html()
