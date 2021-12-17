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
    dates_kreise_orig = dfs[sheet_names[0]].columns[-days:]
    dates_kreise_datetime = tuple(format_to_datetime(x) for x in dates_kreise_orig)
    dates_germany_orig = dfs[sheet_names[1]].columns[-days:]
    dates_germany_datetime = tuple(format_to_datetime(x) for x in dates_germany_orig)
    assert dates_kreise_datetime == dates_germany_datetime

    for df in dfs.values():
        df.index.name = None

    # get results
    df_inzidenz = dfs[sheet_names[0]]
    sort_by_name = lambda landkreis: landkreis.name
    kreise_sorted = list(sorted(kreise, key=sort_by_name))
    df_inzidenz = df_inzidenz.loc[[x.lk_name for x in kreise_sorted], dates_kreise_orig]
    df_inzidenz.columns = dates_kreise_datetime
    df_inzidenz.rename(index=find_landkreis, inplace=True)

    # get germany results
    tmp_ger = dfs[sheet_names[1]].loc["Gesamt", dates_germany_orig]
    tmp_ger.rename(dict(zip(dates_germany_orig, dates_germany_datetime)), inplace=True)
    df_inzidenz.loc[DEUTSCHLAND] = tmp_ger

    # get hositalisierung results if available
    df_hosp = None
    if len(sheet_names) > 2:
        df_hosp = dfs[sheet_names[2]]
        dates_hosp_orig = df_hosp.columns[-days:]
        dates_hosp_datetime = tuple(format_to_datetime(x) for x in dates_hosp_orig)
        assert dates_kreise_datetime == dates_hosp_datetime

        # get results hosp
        laender = list(sorted({x.land for x in kreise if x.land})) + ["Gesamt"]
        df_hosp = df_hosp.loc[laender, dates_hosp_orig]
        df_hosp.columns = dates_hosp_datetime
        df_hosp.rename(index={"Gesamt": DEUTSCHLAND}, inplace=True)

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


async def get_history(landkreise: Collection[Landkreise], fixed_values: bool = False, filename: str=None):
    # get data online
    async with corona.Connector() as con:
        if fixed_values:
            binary_excel = await con.get_excel_fixed()
        else:
            binary_excel = await con.get_excel()
    # read data
    inzidenzen_result, result_hosp = read_excel(binary_excel, landkreise, fixed_values)

    # show data
    last_date = inzidenzen_result.columns[-1]
    inzidenzen_result.rename(columns=date_formatter, inplace=True)
    if result_hosp is not None:
        result_hosp.rename(columns=date_formatter, inplace=True)
    print_result(inzidenzen_result, result_hosp)
    title = set_graph_title(last_date)
    show_graph(inzidenzen_result, result_hosp, title, filename)


def dataframe_max(df: pd.DataFrame, default=0):
    """ returns the max value of DataFrame

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


def get_lines_inz(df: pd.DataFrame):
    """ Returns the lines for inzidenzen which are relevant for warn areas
    https://www.niedersachsen.de/assets/image/216288

    Args:
        df (pd.DataFrame): DataFrame containing all relevant values to display

    Returns:
        list[int]: All lines to display
    """
    max_val = dataframe_max(df)
    result = [x for x in (35,) if x - 5 < max_val]
    result.extend(range(100, int(max_val) + 16, 100))
    return result


def get_lines_hosp(df: pd.DataFrame):
    """ Returns the lines for hospitalisierung which are relevant for warn areas
    https://www.niedersachsen.de/assets/image/216288

    Args:
        df (pd.DataFrame): DataFrame containing all relevant values to display

    Returns:
        list[int]: All lines to display
    """
    max_val = dataframe_max(df)
    result = [x for x in (3, 6, 9) if x - 1 <= max_val]
    result.extend(range(15, int(max_val) + 3, 5))
    return result


def fill_ax(ax, df: pd.DataFrame, hgrid_lines: Collection[int]):
    # plot all items except DEUTSCHLAND
    ax = df.drop(DEUTSCHLAND).T.plot.bar(ax=ax, rot=0)

    # DEUTSCHLAND should appear as line instead of own bar
    series_deutschland = df.loc[DEUTSCHLAND]
    pos = np.array(range(len(series_deutschland.index)))
    ax.hlines(y=series_deutschland, xmin=pos - 0.49, xmax=pos + 0.49, colors="black", label=DEUTSCHLAND)

    ax.legend()

    # should not appear in legend
    for line in hgrid_lines:
        ax.axhline(y=line, color="grey", linestyle="dotted")


def show_graph(df1: pd.DataFrame, df2: pd.DataFrame = None, title: str = None, filename: str = None):
    if df2 is None:
        fig, ax1 = plt.subplots(1, 1)
        hgrid_lines = get_lines_inz(df1)
        fill_ax(ax1, df1, hgrid_lines)
        ax1.set_ylabel("Inzidenz fix")
    else:
        fig, (ax1, ax2) = plt.subplots(2, 1)
        hgrid_lines1 = get_lines_inz(df1)
        fill_ax(ax1, df1, hgrid_lines1)
        hgrid_lines2 = get_lines_hosp(df2)
        fill_ax(ax2, df2, hgrid_lines2)
        ax1.set_ylabel("Inzidenz akt")
        ax2.set_ylabel("Hospitalierung akt")

    if title:
        fig.suptitle(title)

    if filename:
        plt.savefig(filename, bbox_inches='tight')
    else:
        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Corona Inzidenzzahlen Historie")
    PARSER.add_argument("-fix", action="store_true", help="Uses fixed values instead of corrected")
    PARSER.add_argument("-s", "--save", help="Saves as png. Default will just show it.")

    ARGS = PARSER.parse_args()
    FIX = ARGS.fix
    SAVE = ARGS.save
    LANDKREISE = (
        Landkreise.WOLFSBURG,
        Landkreise.OBERBERGISCHER_KREIS,
        Landkreise.KOELN,
        Landkreise.NORDFRIESLAND,
    )
    asyncio.run(get_history(LANDKREISE, FIX, SAVE))
