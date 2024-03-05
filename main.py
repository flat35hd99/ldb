import pandas as pd
from service import ServiceCollection
from controller import Controller
import os


def main():
    # データの読み込み
    dfs = pd.read_excel(
        "DBmaster.xlsx",
        sheet_name=["database", "category", "available_area"],
    )
    database_df = dfs["database"]
    category_df = dfs["category"]
    available_area_df = dfs["available_area"]

    service = ServiceCollection(
        database_df, available_area_df, category_df
    )
    controller = Controller(service)

    # もし output/がなければ作成する
    # そうしないと、後続の処理でファイルを作成・書き込むことができない
    if not os.path.exists("output"):
        os.mkdir("output")

    with open("output/category_jp.html", mode="w", encoding="utf8") as f:
        f.write(
            controller.create_category_html()
        )

    with open("output/alphabet_jp.html", mode="w", encoding="utf8") as f:
        f.write(controller.create_alphabet_html())

    with open("output/category_en.html", mode="w", encoding="utf8") as f:
        f.write(
            controller.create_category_html(
                lang="en"
            )
        )

    with open("output/alphabet_en.html", mode="w", encoding="utf8") as f:
        f.write(controller.create_alphabet_html(lang="en"))


if __name__ == "__main__":
    main()
