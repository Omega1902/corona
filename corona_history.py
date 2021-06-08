from typing import Tuple, List
import requests
import pandas as pd # uses openpyxl in background
import corona


def read_excel(path):
    df = pd.read_excel(path, sheet_name='LK_7-Tage-Inzidenz (fixiert)', engine="openpyxl")

    # date = df.values[0][0]
    lk = (
        "SK Wolfsburg",
        "LK Oberbergischer Kreis",
    )
    result = []
    dates = {}
    read_dates = 14
    for row in df.values:
        if row[1] == "LK":
            pointer = len(row) - 1
            while len(dates) < read_dates:
                if pd.notna(row[pointer]):
                    dates[row[pointer]] = pointer
                pointer -= 1

        elif row[1] in lk:
            temp = {"name": row[1]}
            for date_obj, key in dates.items():
                temp[date_obj] = row[key]
            result.append(temp)

    dates = dict(reversed(list(dates.items())))
    return dates, result

def convert_to_printable_list(dates, inzidenzen) -> Tuple[List[str], List[List[str]]]:
    header = ["Kreise"] + [date_obj.strftime("%d.%m.%Y") for date_obj in dates.keys()]
    table = []

    for row in inzidenzen:
        temp = [row['name']]
        for date_obj in dates.keys():
            temp.append(f"{row[date_obj]:.1f}")
        table.append(temp)
    return header, table


def get_excel(url):
    result = requests.get(url)
    result.raise_for_status()
    return result.content


def get_from_excel():
    binary_excel = get_excel('https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab.xlsx?__blob=publicationFile')
    dates, inzidenzen_result = read_excel(binary_excel)
    header, table = convert_to_printable_list(dates, inzidenzen_result)
    corona.print_table(header, table)


if __name__ == "__main__":
    get_from_excel()
