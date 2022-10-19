from string import Template
import pandas as pd

def divide_into_category(df):
    categories = df["category"].fillna("未分類").unique()
    # If you want sort the order of categories, please create your sorted() function.
    return {category: df[df["category"] == category] for category in sorted(categories)}

def create_category_html():
    output_filepath = ""
    
    with open("templates/category_table.html", encoding="utf8") as f:
        category_table = Template(f.read())
    with open("templates/category_row.html", encoding="utf8") as f:
        category_row = Template(f.read())
    with open("templates/available_remote.html", encoding="utf8") as f:
        available_remote_mark = f.read()

    df = pd.read_excel("db.xlsx")
    
    row = row_factory()
    table = category_table_factory()
    
    table.append_row(row)
    
    table.to_html(output_filepath)

def create_alphabet_html():
    pass

def row_factory():
    pass

def category_table_factory():
    pass

if __name__ == '__main__':
    create_category_html()
    create_alphabet_html()
