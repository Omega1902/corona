from typing import Collection, Tuple, List, Optional, Sequence
from datetime import datetime
import asyncio
import pandas as pd  # uses openpyxl in background
import matplotlib.pyplot as plt
import numpy as np
import corona
from landkreise import Landkreise


def format_to_datetime(excel_date):
    if isinstance(excel_date, datetime):
        return excel_date
    if isinstance(excel_date, str):
        return datetime.strptime(excel_date, "%d.%m.%Y")
    # hope it's int
    return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date) - 2)


def read_excel(path, kreise: Collection[str], days: int = 8):
    # read kreise
    data_frame = pd.read_excel(path, sheet_name="LK_7-Tage-Inzidenz (fixiert)", engine="openpyxl")

    result = []
    dates = {}
    for row in data_frame.values:
        if row[1] == "LK":
            pointer = len(row) - 1
            while len(dates) < days:
                if pd.notna(row[pointer]):
                    dates[format_to_datetime(row[pointer])] = pointer
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
        if row_number == 3:
            pointer = len(row) - 1
            while len(dates_germany) < days:
                if pd.notna(row[pointer]):
                    dates_germany[format_to_datetime(row[pointer])] = pointer
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
        temp = [str(Landkreise.find_by_lk_name(row["name"]))]
        for date_obj in dates:
            temp.append(f"{row[date_obj]:.1f}")
        table.append(temp)
    return header, table


def convert_to_graph_data(dates, inzidenzen) -> Tuple[List[str], List[str], List[List[float]]]:
    axis_labels = [date_obj.strftime("%d.%m.") for date_obj in dates]
    kreis = []
    table = []

    for row in inzidenzen:
        kreis.append(str(Landkreise.find_by_lk_name(row["name"])))
        table.append([row[date_obj] for date_obj in dates])

    return axis_labels, kreis, table


def set_graph_title(dates):
    return "7-Tages Inzidenzwerte, Stand: " + dates[-1].strftime("%d.%m.%Y")


def print_result(dates, inzidenzen_result):
    header, table = convert_to_printable_list(dates, inzidenzen_result)
    corona.print_table(header, table)


def plot_result(dates, inzidenzen_result, germany_result):
    x_axis_labels, kreis, graph_data = convert_to_graph_data(dates, inzidenzen_result)
    germany_inzidenzen = [value for (_, value) in sorted(germany_result.items())]
    title = set_graph_title(dates)
    show_graph(graph_data, kreis, x_axis_labels, title, compare_line=germany_inzidenzen)


async def get_history(landkreise: Collection[Landkreise]):
    # get data online
    async with corona.Connector() as con:
        binary_excel = await con.get_excel()
    # read data
    dates, inzidenzen_result, germany_result = read_excel(binary_excel, tuple(lk.lk_name for lk in landkreise))
    # show data
    print_result(dates, inzidenzen_result)
    plot_result(dates, inzidenzen_result, germany_result)


def get_lines(groups: List[List[float]], compare_line: Optional[Collection[float]] = None):
    max_comp = 0 if not compare_line else max(compare_line)
    max_val = 0 if not groups else max((0 if not group else max(group) for group in groups))
    max_val = max(max_val, max_comp)
    result = [x for x in (10, 35, 50) if x - 5 < max_val]
    result.extend(range(100, int(max_val) + 16, 50))
    return result


def show_graph(
    groups: List[List[float]],
    group_labels: Optional[Sequence[str]] = None,
    x_axis_labels: Optional[Sequence[str]] = None,
    title: Optional[str] = None,
    suptitle: Optional[str] = None,
    compare_line: Optional[Sequence[float]] = None,
):
    size = len(groups)
    assert size > 0, "groups should not be empty"
    if group_labels is not None:
        assert len(group_labels) == size, "the ammount of groups and group_labels should match"
    if x_axis_labels is not None:
        assert len(x_axis_labels) == len(groups[0]), "the ammount of groups data and group_labels should match"

    width = 0.8 / size
    adjust_width = -1 * width * (size - 1) / 2

    pos = np.array(range(len(groups[0])))

    for i in range(size):
        if group_labels:
            plt.bar(pos + i * width + adjust_width, groups[i], width=width, label=group_labels[i])
        else:
            plt.bar(pos + i * width + adjust_width, groups[i], width=width)

    if x_axis_labels is not None:
        plt.xticks(pos, x_axis_labels)

    if title is not None:
        plt.title(title)

    if suptitle is not None:
        plt.suptitle(suptitle)

    if compare_line is not None:
        assert len(groups[0]) == len(compare_line), "the ammount of compare lines should match the amount of groups data"
        plt.hlines(y=compare_line, xmin=pos - 0.49, xmax=pos + 0.49, colors="black", label="Deutschland")

    plt.legend()

    for line in get_lines(groups, compare_line):
        plt.axhline(y=line, color="grey", linestyle="dotted")

    # plt.grid(True, which="major" , axis="y")

    plt.show()


if __name__ == "__main__":
    LANDKREISE = (
        Landkreise.WOLFSBURG,
        Landkreise.OBERBERGISCHER_KREIS,
        Landkreise.KOELN,
        Landkreise.NORDFRIESLAND,
    )
    asyncio.run(get_history(LANDKREISE))
