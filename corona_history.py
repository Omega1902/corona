from typing import Iterable, Tuple, List, Optional
import asyncio
import pandas as pd # uses openpyxl in background
import matplotlib.pyplot as plt
import numpy as np
import corona

def read_excel(path, kreise, days = 14):
    data_frame = pd.read_excel(path, sheet_name='LK_7-Tage-Inzidenz (fixiert)', engine="openpyxl")

    result = []
    dates = {}
    for row in data_frame.values:
        if row[1] == "LK":
            pointer = len(row) - 1
            while len(dates) < days:
                if pd.notna(row[pointer]):
                    dates[row[pointer]] = pointer
                pointer -= 1

        elif row[1] in kreise:
            temp = {"name": row[1]}
            for date_obj, key in dates.items():
                temp[date_obj] = row[key]
            result.append(temp)

    dates = {key: dates[key] for key in sorted(dates.keys())}
    return dates, result

def convert_to_printable_list(dates, inzidenzen) -> Tuple[List[str], List[List[str]]]:
    header = ["Kreise"] + [date_obj.strftime("%d.%m.") for date_obj in dates.keys()]
    table = []

    for row in inzidenzen:
        temp = [row['name']]
        for date_obj in dates.keys():
            temp.append(f"{row[date_obj]:.1f}")
        table.append(temp)
    return header, table

def convert_to_graph_data(dates, inzidenzen) -> Tuple[List[str], List[str], List[List[int]]]:
    axis_labels = [date_obj.strftime("%d.%m.") for date_obj in dates.keys()]
    kreis = []
    table = []

    for row in inzidenzen:
        kreis.append(row['name'])
        temp = []
        for date_obj in dates.keys():
            temp.append(row[date_obj])
        table.append(temp)
    return axis_labels, kreis, table


async def get_from_excel():
    kreise = (
        "SK Wolfsburg",
        "LK Oberbergischer Kreis",
        "SK Köln",
    )

    async with corona.Connector() as con:
        binary_excel = await con.get_excel()
    dates, inzidenzen_result = read_excel(binary_excel, kreise)
    header, table = convert_to_printable_list(dates, inzidenzen_result)
    corona.print_table(header, table)
    x_axis_labels, kreis, graph_data = convert_to_graph_data(dates, inzidenzen_result)
    suptitle = "7-Tages Inzidenzwerte"
    title = "Stand: " + x_axis_labels[-1]
    show_graph(graph_data, kreis, x_axis_labels, title, suptitle)

def show_graph(groups: List[List[int]], group_labels: Optional[Iterable[str]] = None, x_axis_labels: Optional[Iterable[str]] = None, title: Optional[str] = None, suptitle: Optional[str] = None):
    size = len(groups)
    assert size > 0, "groups should not be empty"
    if group_labels is not None:
        assert len(group_labels) == size, "the ammount of groups and group_labels should match"
    if x_axis_labels is not None:
        assert len(x_axis_labels) == len(groups[0]), "the ammount of groups data and group_labels should match"

    width = 0.8 / size
    adjust_width = -1 * width * (size -1) / 2

    pos = np.array(range(len(groups[0])))

    for i in range(size):
        plt.bar(pos + i * width + adjust_width, groups[i], width=width)

    if x_axis_labels is not None:
        plt.xticks(pos, x_axis_labels)

    if group_labels is not None:
        plt.legend(group_labels)

    if title is not None:
        plt.title(title)

    if suptitle is not None:
        plt.suptitle(suptitle)

    # plt.grid(True, which="major" , axis="y")

    plt.show()


if __name__ == "__main__":
    asyncio.run(get_from_excel())
