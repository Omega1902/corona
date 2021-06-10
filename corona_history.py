from landkreise import Landkreise
from typing import Collection, Tuple, List, Optional
import asyncio
import pandas as pd # uses openpyxl in background
import matplotlib.pyplot as plt
import numpy as np
import corona

def read_excel(path, kreise: Collection[str], days: int = 7):
    # read kreise
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


    # read Deutschland
    data_frame = pd.read_excel(path, sheet_name="BL_7-Tage-Inzidenz (fixiert)", engine="openpyxl")
    germany = {}
    dates_germany = {}
    for row_number, row in enumerate(data_frame.values):
        if row_number == 1:
            pointer = len(row) - 1
            while len(dates_germany) < days:
                if pd.notna(row[pointer]):
                    dates_germany[row[pointer]] = pointer
                pointer -= 1
        elif row[0] == "Gesamt":
            for date_obj, key in dates_germany.items():
                germany[date_obj] = row[key]

    assert dates.keys() == dates_germany.keys()
    return sorted(dates.keys()), result, germany

def convert_to_printable_list(dates, inzidenzen) -> Tuple[List[str], List[List[str]]]:
    header = ["Kreise"] + [date_obj.strftime("%d.%m.") for date_obj in dates]
    table = []

    for row in inzidenzen:
        temp = [str(Landkreise.find_by_lk_bez(row['name']))]
        for date_obj in dates:
            temp.append(f"{row[date_obj]:.1f}")
        table.append(temp)
    return header, table

def convert_to_graph_data(dates, inzidenzen) -> Tuple[List[str], List[str], List[List[int]]]:
    axis_labels = [date_obj.strftime("%d.%m.") for date_obj in dates]
    kreis = []
    table = []

    for row in inzidenzen:
        kreis.append(str(Landkreise.find_by_lk_bez(row['name'])))
        temp = []
        for date_obj in dates:
            temp.append(row[date_obj])
        table.append(temp)

    return axis_labels, kreis, table

def convert_germany_to_graph_data(germany_result):
    germany_result


async def get_from_excel(landkreise: Collection[Landkreise]):
    async with corona.Connector() as con:
        binary_excel = await con.get_excel()
    dates, inzidenzen_result, germany_result = read_excel(binary_excel, tuple(lk.lk_name for lk in landkreise))
    header, table = convert_to_printable_list(dates, inzidenzen_result)
    corona.print_table(header, table)
    x_axis_labels, kreis, graph_data = convert_to_graph_data(dates, inzidenzen_result)
    germany_inzidenzen = [value for (key, value) in sorted(germany_result.items())]
    title = "7-Tages Inzidenzwerte, Stand: " + x_axis_labels[-1]
    show_graph(graph_data, kreis, x_axis_labels, title, compare_line=germany_inzidenzen)

def show_graph(groups: List[List[int]], group_labels: Optional[Collection[str]] = None, x_axis_labels: Optional[Collection[str]] = None, title: Optional[str] = None, suptitle: Optional[str] = None, compare_line: Optional[Collection[int]] = None):
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

    if compare_line is not None:
        assert len(groups[0]) == len(compare_line), "the ammount of compare lines should match the amount of groups data"
        for i, cur_line in enumerate(compare_line):
            plt.hlines(y=cur_line, xmin=pos[i] - 0.49, xmax=pos[i] + 0.49)

    plt.axhline(y=35)
    plt.axhline(y=50)

    # plt.grid(True, which="major" , axis="y")

    plt.show()


if __name__ == "__main__":
    LANDKREISE = (
        Landkreise.WOLFSBURG,
        Landkreise.OBERBERGISCHER_KREIS,
        Landkreise.KOELN,
        Landkreise.NORDFRIESLAND,
    )
    asyncio.run(get_from_excel(LANDKREISE))
