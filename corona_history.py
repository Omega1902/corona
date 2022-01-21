from typing import Collection
from datetime import datetime
import argparse
import asyncio
import re
import pandas as pd  # uses xlrd in background
import matplotlib.pyplot as plt
import numpy as np
import corona
from landkreise import Landkreise, DEUTSCHLAND


def find_landkreis(lk_name: str):
    res = Landkreise.find_by_lk_name(lk_name)
    return res if res is not None else lk_name


def format_to_datetime(excel_date):
    if isinstance(excel_date, datetime):
        return excel_date
    if isinstance(excel_date, str):
        return datetime.strptime(excel_date, "%d.%m.%Y")
    # hope it's int
    return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date) - 2)


def read_excel(path, kreise: Collection[Landkreise], fixed_values: bool = False, days: int = 8):
    def my_use_cols(index):
        if index in ("Unnamed: 0", "LK", "MeldeLandkreisBundesland", "MeldeLandkreis"):
            return True
        if isinstance(index, datetime):
            return True
        if isinstance(index, str):
            return bool(re.match(r"\d{1,2}.\d{1,2}.\d{4}", index))
        return False

    if fixed_values:
        sheet_names = ["LK_7-Tage-Inzidenz (fixiert)", "BL_7-Tage-Inzidenz (fixiert)"]
        skip_rows = 4
    else:
        sheet_names = ["LK_7-Tage-Inzidenz-aktualisiert", "BL_7-Tage-Inzidenz-aktualisiert", "BL_7-Tage-Inzidenz Hosp(aktual)"]
        skip_rows = 2
    dfs = pd.read_excel(path, sheet_name=sheet_names, index_col=0, usecols=my_use_cols, skiprows=skip_rows, engine="xlrd")

    for df in dfs.values():
        df.index.name = None

    # get results
    df_inzidenz = dfs[sheet_names[0]]
    sort_by_name = lambda landkreis: landkreis.name
    kreise_sorted = list(sorted(kreise, key=sort_by_name))
    df_inzidenz = df_inzidenz.loc[[x.lk_name for x in kreise_sorted], df_inzidenz.columns[-days:]]
    df_inzidenz.rename(index=find_landkreis, columns=format_to_datetime, inplace=True)

    # get germany results
    tmp_ger = dfs[sheet_names[1]].loc["Gesamt", dfs[sheet_names[1]].columns[-days:]]
    tmp_ger.rename(format_to_datetime, inplace=True)
    df_inzidenz.loc[DEUTSCHLAND] = tmp_ger

    # get hositalisierung results if available
    df_hosp = None
    if len(sheet_names) > 2:
        df_hosp = dfs[sheet_names[2]]

        # get results hosp
        laender = list(sorted({x.land for x in kreise if x.land})) + ["Gesamt"]
        df_hosp = df_hosp.loc[laender, df_hosp.columns[-days:]]
        df_hosp.rename(index={"Gesamt": DEUTSCHLAND}, columns=format_to_datetime, inplace=True)

        pd.testing.assert_index_equal(df_inzidenz.columns, df_hosp.columns)

    return df_inzidenz, df_hosp


def print_result(df1, df2=None):
    # format ouput
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    # pd.set_option('display.max_colwidth', -1)
    pd.set_option("display.precision", 1)

    # show data
    print(df1)
    if df2 is not None:
        print()
        print(df2)


def date_formatter(date_obj):
    return date_obj.strftime("%d.%m.")


def set_graph_title(date_obj):
    return "7-Tages Inzidenzwerte, Stand: " + date_obj.strftime("%d.%m.%Y")


async def get_history(landkreise: Collection[Landkreise], fixed_values: bool = False, output_file: str = None, method=8, input_file: str = None):
    """Corona Inzidenzzahlen Historie

    Args:
        landkreise (Collection[Landkreise]): The landkreise to get
        fixed_values (bool, optional): Whether to use the fixed inzident values or not. Defaults to False.
        output_file (str, optional): Will save plot as imp with given name. If empty or None the plot will just be displayed. Defaults to None.
        method (str|int, optional): If set to an int, will use these as days to plot.
                                    If set to 'w' or 'week', will plot all weeks.
                                    If set to 'm' or 'month', will plot all months. Defaults to 8.
        input_file (str, optional): Will save plot as imp with given name. If empty or None the plot will just be displayed. Defaults to None.
    """

    if input_file:
        with open(input_file, "br") as excel_file:
            binary_excel = excel_file.read()
    else:
        # get data online
        async with corona.Connector() as con:
            if fixed_values:
                binary_excel = await con.get_excel_fixed()
            else:
                binary_excel = await con.get_excel()
    # read data
    days = 0
    try:
        method = 8 if method is None else int(method)
        days = method
    except ValueError:
        pass
    inzidenzen_result, result_hosp = read_excel(binary_excel, landkreise, fixed_values, days)

    # show data
    if isinstance(method, int):
        last_date = inzidenzen_result.columns[-1]
        inzidenzen_result.rename(columns=date_formatter, inplace=True)
        if result_hosp is not None:
            result_hosp.rename(columns=date_formatter, inplace=True)
        print_result(inzidenzen_result, result_hosp)
        title = set_graph_title(last_date)
        show_graph(inzidenzen_result, result_hosp, title, output_file)
    else:
        show_boxplot(inzidenzen_result.T, method, output_file)


def dataframe_max(df: pd.DataFrame, default=0):
    """returns the max value of DataFrame

    Args:
        df (pd.DataFrame): DataFrame containing numbers
        default (number): Returned if there are no values or df is None. Defaults to 0.

    Returns:
        number: Max value. If there are no values or df is None returns default
    """
    max_val = default if df is None else df.max().max()
    if pd.isna(max_val):
        max_val = default
    return max_val


def get_lines_inz(max_val: float):
    """Returns the lines for inzidenzen which are relevant for warn areas
    https://www.niedersachsen.de/assets/image/216288

    Args:
        max_val (int|float): Max value

    Returns:
        list[int]: All lines to display
    """
    result = [x for x in (35,) if x - 5 < max_val]
    result.extend(range(100, int(max_val) + 16, 100))
    return result


def get_lines_hosp(max_val: float):
    """Returns the lines for hospitalisierung which are relevant for warn areas
    https://www.niedersachsen.de/assets/image/216288

    Args:
        max_val (int|float): Max value

    Returns:
        list[int]: All lines to display
    """
    result = [x for x in (3, 6, 9) if x - 1 <= max_val]
    result.extend(range(15, int(max_val) + 3, 5))
    return result


def save_or_show(output_file: str = None, fig=None):
    if output_file:
        plt.savefig(output_file, bbox_inches="tight")
    else:
        if fig:
            fig.tight_layout()
        plt.show()


def _get_colors(min_values: Collection[int], max_values: Collection[int], count: int):
    result = np.linspace(min_values, max_values, count)
    return [f"#{int(round(res[0])):02x}{int(round(res[1])):02x}{int(round(res[2])):02x}" for res in result]


def get_colors(df1, df2):
    # colors
    all_colors = pd.DataFrame(
        (
            ("2blue", "min", 0, 0, 170),
            ("2blue", "max", 64, 166, 255),
            ("5yellow", "min", 202, 149, 32),
            ("5yellow", "max", 221, 221, 0),
            # ("2orange", "min", 216, 75, 32),
            # ("2orange", "max", 255, 144, 43),
            ("1green", "min", 30, 117, 29),
            ("1green", "max", 37, 231, 18),
            ("3violet", "min", 153, 00, 153),
            ("3violet", "max", 222, 124, 222),
            ("4brown", "min", 76, 47, 38),
            ("4brown", "max", 180, 125, 73),
            ("6red", "min", 136, 0, 0),
            ("6red", "max", 241, 86, 71),
        ),
        columns=("name", "type", "r", "g", "b"),
    )
    all_colors.set_index(["name", "type"], inplace=True)
    # all_hatches = ("", "/", "\\", "x")
    bundeslaender = df2.index.drop(DEUTSCHLAND)
    colors_count = min(len(bundeslaender), len(all_colors) // 2)
    color_indexes = all_colors.index.levels[0]

    all_lks = df1.index.drop(DEUTSCHLAND)
    result_lks = {}
    result_bundesland = {}
    for i, bundesland in enumerate(bundeslaender):
        color_name = color_indexes[i % colors_count]
        color_df = all_colors.loc[color_name]
        lks = [lk for lk in all_lks if lk.land == bundesland]
        color_variations = max(len(lks) + 1, 7)
        colors = _get_colors(color_df.loc["min"].values, color_df.loc["max"].values, color_variations)
        result_bundesland[bundesland] = colors.pop(len(colors) // 2)
        if len(lks) == 1:
            result_lks[lks[0]] = result_bundesland[bundesland]
        else:
            for lk in lks:
                result_lks[lk] = colors.pop(len(colors) // 2)

    return result_lks, result_bundesland


def fill_ax(ax, df: pd.DataFrame, hgrid_lines: Collection[int], colors=None):
    # plot all items except DEUTSCHLAND
    ax = df.drop(DEUTSCHLAND).T.plot.bar(ax=ax, rot=0, color=colors)

    # DEUTSCHLAND should appear as line instead of own bar
    series_deutschland = df.loc[DEUTSCHLAND]
    pos = np.array(range(len(series_deutschland.index)))
    ax.hlines(y=series_deutschland, xmin=pos - 0.49, xmax=pos + 0.49, colors="black", label=DEUTSCHLAND)

    ax.legend()

    # should not appear in legend
    for line in hgrid_lines:
        ax.axhline(y=line, color="grey", linestyle="dotted")


def get_bg_colors(max_val: float, hgrid_lines: Collection[float], column_count: int):
    result = []
    bgcolors = ("#00ff00", "#ffff00", "#ffa500", "#ff0000")
    data_count = 2
    x = [-0.5, column_count + 0.5]
    y1 = [0] * data_count
    if not hgrid_lines:  # no hgrid lines
        y2 = [max_val] * data_count
        temp = (x, y1, y2, bgcolors[0])
        result.append(temp)
        return result
    y2 = y1
    for i, line in enumerate(hgrid_lines):
        y1 = y2
        if i + 1 == len(bgcolors):  # if last bgcolor set higher border to highest value
            line = max(hgrid_lines[-1], max_val)
        y2 = [line] * data_count
        color = bgcolors[i]
        temp = (x, y1, y2, color)
        result.append(temp)
        if i + 1 == len(bgcolors):
            return result  # returns if all bgcolors have been used
    if len(hgrid_lines) < len(bgcolors) and max_val > hgrid_lines[-1]:
        y1 = y2
        y2 = [max_val] * data_count
        color = bgcolors[len(hgrid_lines)]
        temp = (x, y1, y2, color)
        result.append(temp)
    return result


def add_bg_colors(ax, max_val, hgrid_lines, column_count: int):
    bg_colors = get_bg_colors(max_val, hgrid_lines, column_count)
    for bg_color in bg_colors:
        ax.fill_between(bg_color[0], bg_color[1], bg_color[2], alpha=0.2, linewidth=0, color=bg_color[3])


def show_graph(df1: pd.DataFrame, df2: pd.DataFrame = None, title: str = None, output_file: str = None):
    if df2 is None:
        # calc horizontal grid lines
        max_val = dataframe_max(df1)
        hgrid_lines = get_lines_inz(max_val)

        # plot
        fig, ax1 = plt.subplots(1, 1)
        add_bg_colors(ax1, max_val, hgrid_lines, len(df1.columns))
        fill_ax(ax1, df1, hgrid_lines)
        ax1.set_ylabel("Inzidenz fix")
    else:
        # colors and lines
        colors_ax1, colors_ax2 = get_colors(df1, df2)
        max_val1 = dataframe_max(df1)
        max_val2 = dataframe_max(df2)
        hgrid_lines1 = get_lines_inz(max_val1)
        hgrid_lines2 = get_lines_hosp(max_val2)

        # plot
        fig, (ax1, ax2) = plt.subplots(2, 1)
        add_bg_colors(ax1, max_val1, hgrid_lines1, len(df1.columns))
        add_bg_colors(ax2, max_val2, hgrid_lines2, len(df2.columns))
        fill_ax(ax1, df1, hgrid_lines1, colors_ax1)
        fill_ax(ax2, df2, hgrid_lines2, colors_ax2)
        ax1.set_ylabel("Inzidenz akt")
        ax2.set_ylabel("Hospitalierung akt")

    if title:
        fig.suptitle(title)

    save_or_show(output_file, fig)


def _filter_by_min(df: pd.DataFrame, column, mininmum: int):
    counts = df[column].value_counts()
    return df[df[column].isin(counts[counts >= mininmum].index)]


def by_month(df: pd.DataFrame, **kwargs):
    month_str = lambda date_obj: date_obj.strftime("%Y-%m")
    df["Monat"] = df.index.to_series().apply(month_str)
    df = _filter_by_min(df, "Monat", 7)
    return df.boxplot(by="Monat", **kwargs)


def format_to_week(date_obj: datetime):
    """Formats like date_obj to YYYY-WW using isocalendar(). Therefore the calendar week is between "01" and "53", e.g. datetime(2021, 1, 3) -> "2020-53"

    Args:
        date_obj (datetime.datetime): Datetime object to format

    Returns:
        str: String representation of the calendar week including year "YYYY-WW"
    """
    year, month, _ = date_obj.isocalendar()
    return f"{year}-{month:02}"


def by_week(df: pd.DataFrame, **kwargs):
    df["KW"] = df.index.to_series().apply(format_to_week)
    df = _filter_by_min(df, "KW", 3)
    return df.boxplot(by="KW", **kwargs)


def show_boxplot(df: pd.DataFrame, method: str, output_file: str = None):
    if method.lower().startswith("m"):
        axes_series_2dim = by_month(df, rot=45)
    elif method.lower().startswith("w"):
        axes_series_2dim = by_week(df, rot=45)
    else:
        raise ValueError("method does not start with 'w' or 'm'!")
    for axes_series in axes_series_2dim:
        if isinstance(axes_series, (pd.Series, np.ndarray)):
            for ax in axes_series:
                ax.set_ylim(bottom=0)
        else:
            axes_series.set_ylim(bottom=0)

    save_or_show(output_file)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Corona Inzidenzzahlen Historie")
    PARSER.add_argument("-fix", action="store_true", help="Uses fixed values instead of corrected")
    PARSER.add_argument("-s", "--save", help="Saves as png with given filename. Default will just show it.")
    PARSER.add_argument(
        "-t",
        "--type",
        help="If set to an int, will use these as days to plot. If set to 'w' or 'week', will plot all weeks. If set to 'm' or 'month', will plot all months.",
    )
    PARSER.add_argument("-i", "--input", help="If set will use this as input-excel file. '-fix' parameter must be set accordingly.")

    ARGS = PARSER.parse_args()
    FIX = ARGS.fix
    SAVE = ARGS.save
    TYPE = ARGS.type
    INPUT = ARGS.input
    LANDKREISE = (
        Landkreise.WOLFSBURG,
        Landkreise.OBERBERGISCHER_KREIS,
        Landkreise.KOELN,
        Landkreise.NORDFRIESLAND,
    )
    asyncio.run(get_history(LANDKREISE, FIX, SAVE, TYPE, INPUT))
