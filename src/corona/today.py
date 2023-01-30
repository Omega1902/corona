import argparse
import asyncio
import logging
from typing import AsyncIterable, Iterable, Optional

from corona.landkreise import Landkreise
from corona.rki_connector import CasesResult, Connector

LOG = logging.getLogger(__name__)


async def print_result_async(cities: AsyncIterable[CasesResult], column1_width: int = 20) -> None:
    date_string = None
    print_format = "{:" + str(column1_width) + "} {:>8}"
    async for city in cities:
        if date_string is None:
            date_string = city.updated[:10]
            print(f"Datum: {date_string}")
            print(print_format.format("Landkreis", "Inzidenz"))
        elif not city.updated.startswith(date_string):
            raise RuntimeError("Different updated dates!")
        print(print_format.format(city.city_name, f"{city.cases7_per_100k:3.2f}"))


async def print_result_async2(result: AsyncIterable[CasesResult], print_id: bool = False) -> None:
    to_print = []
    date_string = None
    async for city in result:
        if date_string is None:
            date_string = city.updated[:10]
        elif not city.updated.startswith(date_string):
            raise RuntimeError("Different updated dates!")
        temp = []
        if print_id:
            temp.append(f"{city.county} ({city.region_id})")
        else:
            temp.append(city.city_name)
        temp.append(f"{city.cases7_per_100k:3.2f}")
        to_print.append(temp)
    if date_string is None:
        print("Keine Daten verfügbar")
    else:
        print(f"Datum: {date_string}")
        header = ["Landkreis", "Inzidenz"]
        print_table(header, to_print)


def print_result(result: Iterable[CasesResult], print_id: bool = False) -> None:
    to_print = []
    date_string = None
    for city in result:
        if date_string is None:
            date_string = city.updated[:10]
        elif not city.updated.startswith(date_string):
            raise RuntimeError("Different updated dates!")
        temp = []
        if print_id:
            temp.append(f"{city.county} ({city.region_id})")
        else:
            temp.append(city.city_name)
        temp.append(f"{city.cases7_per_100k:3.2f}")
        to_print.append(temp)
    if date_string is None:
        print("Keine Daten verfügbar")
    else:
        print(f"Datum: {date_string}")
        header = ["Landkreis", "Inzidenz"]
        print_table(header, to_print)


def print_table(headers: list[str], table: list[list[str]]) -> None:
    print_formats = []
    for i, header in enumerate(headers):
        size = max(len(x[i]) for x in table)
        size = max(size, len(header))
        if i == 0:  # First item left binding
            print_formats.append("{:" + str(size) + "}")
        else:  # all other right binding
            print_formats.append("{:>" + str(size) + "}")
    print_format = " ".join(print_formats)
    LOG.debug("Format: '%s'", print_format)
    print(print_format.format(*headers))
    for row in table:
        print(print_format.format(*row))


async def handle_context_manager(con_needs_opening: bool, con: Connector, coro_func, *args, **kwargs):
    if con_needs_opening:
        async with con:
            return await coro_func(*args, **kwargs)
    return await coro_func(*args, **kwargs)


async def get_and_print_landkreise_tasks(con, landkreise: Iterable[Landkreise], force_order: bool) -> None:
    async_generator = con.get_cases(landkreise, force_order)
    if force_order:
        await print_result_async2(async_generator)
    else:
        await print_result_async(async_generator)


async def main(
    landkreise: Optional[Iterable[Landkreise]] = None, keep_order: bool = False, con: Optional[Connector] = None
) -> None:
    con_needs_opening = False
    if con is None:
        con = Connector()
        con_needs_opening = True
    if landkreise is None:
        result = await handle_context_manager(con_needs_opening, con, con.get_all_cases)
        sort_by_name = lambda city: city.city_name
        result.sort(key=sort_by_name)
        print_result(result, True)
    else:
        await handle_context_manager(
            con_needs_opening, con, get_and_print_landkreise_tasks, con, landkreise, keep_order
        )
    await asyncio.sleep(0.15)  # prevents "RuntimeError: Event loop is closed"


async def wrapped_main(default_regions: Iterable[Landkreise]) -> None:
    parser = argparse.ArgumentParser(description="Corona Inzidenzzahlen")
    parser.add_argument(
        "-ids",
        "--region_ids",
        type=int,
        nargs="*",
        help="Region Ids für Regionen die geprüft werden sollen. Default verwendet im Skript hintelegte Ids. "
        "Es funktionieren nur bekannte ids.",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Gibt alle Inzidenzzahlen inkl Region IDs aus. Ignoriert die anderen Parameter.",
    )
    parser.add_argument(
        "-o", "--force_order", action="store_true", help="Ausgabe ist in der selben Reihenfolge wie die IDs."
    )

    args = parser.parse_args()

    if args.region_ids is not None:
        default_regions = Landkreise.find_by_ids(args.region_ids)
    if args.all:
        default_regions = None

    await main(default_regions, args.force_order)


if __name__ == "__main__":
    logging.basicConfig(
        # level=logging.DEBUG,
        format="%(asctime)s %(name)-22s %(levelname)-8s %(message)s",
    )

    REGIONS = (
        Landkreise.BERLIN_MITTE,
        Landkreise.HANNOVER,
        Landkreise.AURICH,
        Landkreise.NORDFRIESLAND,
        Landkreise.LUEBECK,
        Landkreise.HAMBURG,
        Landkreise.WOLFSBURG,
        Landkreise.OBERBERGISCHER_KREIS,
        Landkreise.KOELN,
        Landkreise.OSTHOLSTEIN,
    )

    asyncio.run(wrapped_main(REGIONS))
