import pandas as pd
import requests
from bs4 import BeautifulSoup


def main():
    base_url = "https://www.nul.nagoya-u.ac.jp/db"
    soup_abc = BeautifulSoup(
        requests.get(f"{base_url}/index.html").content,
        "html.parser",
        from_encoding="utf-8",
    )

    tables = soup_abc.findAll("table")
    df = pd.DataFrame(columns=["name", "url", "category"])

    for table in tables[1:]:
        rows = table.find("tbody").findAll("tr")
        rows = rows[2:]
        for row in rows:
            tabledatas = row.findAll("td")
            if len(tabledatas) < 5:
                continue
            name_column = tabledatas[0]
            area_column = tabledatas[1]
            remote_column = tabledatas[2]
            simultaneous_connections_column = tabledatas[3]
            guide_column = tabledatas[4]

            dictionary = {
                "name": None,
                "url": None,
                "category": table["summary"],
                "available_area": area_column.text,
                "is_available_remote": len(remote_column.text) == 1,
                "simultaneous_connections": simultaneous_connections_column.text
                if len(simultaneous_connections_column.text) != 0
                and simultaneous_connections_column.text != " "
                else -1,
                "access_color": None,
                "guide": guide_column.text if guide_column.text != " " else None,
            }

            try:
                dictionary["name"] = " ".join(name_column.find("a").text.split())
                dictionary["url"] = name_column.find("a")["href"]
            except Exception as e:
                dictionary["name"] = "no_link"
                dictionary["url"] = "no_link"

            if "line-green" in row["class"]:
                dictionary["access_color"] = "green"
            elif "line-yellow" in row["class"]:
                dictionary["access_color"] = "yellow"
            else:
                dictionary["access_color"] = "red"

            df = df.append(dictionary, ignore_index=True)
    df.to_csv("category.csv", index=False)


if __name__ == "__main__":
    main()
