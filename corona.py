import argparse
import asyncio
import logging
import os
from collections import namedtuple
from typing import Iterable, Optional

import aiohttp  # pip install aiohttp OPTIONAL: pip install aiodns

from landkreise import Landkreise

CasesResult = namedtuple("CasesResult", ("city_name", "county", "cases7_per_100k", "updated", "region_id"))


class Connector:
    def __init__(self):
        fields = (
            "OBJECTID",
            "GEN",
            # 'BEZ',
            # 'BL',
            "county",
            # 'cases',
            # 'deaths',
            # 'cases_per_population',
            "cases7_per_100k",
            # 'cases7_lk',
            # 'death7_lk',
            # 'cases7_bl_per_100k',
            # 'cases7_bl',
            # 'death7_bl',
            "last_update",
        )
        fieldstr = ",".join(fields)

        self.url = (
            "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/"
            f"RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID={{}}&outFields={fieldstr}&returnGeometry=false&outSR=&f=json"
        )
        self.url_all = (
            "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/"
            f"RKI_Landkreisdaten/FeatureServer/0/query?where=1=1&outFields={fieldstr}&returnGeometry=false&outSR=&f=json"
        )
        excel_urls = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/"
        self.url_excel = f"{excel_urls}Fallzahlen_Inzidenz_aktualisiert.xlsx?__blob=publicationFile"
        self.url_excel_fixed = f"{excel_urls}Fallzahlen_Kum_Tab_aktuell.xlsx?__blob=publicationFile"
        self.url_excel_fixed_archive = f"{excel_urls}Fallzahlen_Kum_Tab_Archiv.xlsx?__blob=publicationFile"

        self.url_germany = (
            "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/"
            "rki_key_data_v/FeatureServer/0/query?f=json&where=ObjectId=1&returnGeometry=false&outFields=Inz7T"
        )
        self._session = None
        self.proxy = os.getenv("HTTP_PROXY")

    @classmethod
    def parse_answer(cls, response_json) -> CasesResult:
        results = cls.parse_answer_all(response_json)
        if len(results) != 1:
            raise RuntimeError(f"length of results does not match, expected 1 and got {len(results)}")
        return results[0]

    @staticmethod
    def parse_answer_all(response_json) -> list[CasesResult]:
        result = []
        for city in response_json["features"]:
            region_id = city["attributes"]["OBJECTID"]
            bereich = city["attributes"]["GEN"]
            county = city["attributes"]["county"]
            cases7_per_100k = city["attributes"]["cases7_per_100k"]
            last_update = city["attributes"]["last_update"]
            result.append(CasesResult(bereich, county, cases7_per_100k, last_update, region_id))
        return result

    def get(self, url):
        return self._session.get(url, proxy=self.proxy)

    async def get_case(self, landkreis: Landkreise):
        url = self.url.format(landkreis.id)
        logging.info("Url: '%s'", url)
        async with self.get(url) as response:
            response_json = await response.json()
        logging.debug("%i loaded", landkreis.id)
        response = self.parse_answer(response_json)
        if response.county != landkreis.lk_name:
            raise RuntimeError(f"Wrong lk_name was returned: requested {landkreis.lk_name}, returned {response.county}")
        if response.region_id != landkreis.id:
            raise RuntimeError(f"Wrong id was returned: requested {landkreis.id}, returned {response.region_id}")
        return response

    async def get_cases(self, landkreise: Iterable[Landkreise]):
        coros = tuple(map(self.get_case, landkreise))
        return await asyncio.gather(*coros)

    async def get_all_cases(self):
        async with self.get(self.url_all) as response:
            response_json = await response.json()
        logging.debug("Loaded: %s", str(response_json))
        return self.parse_answer_all(response_json)

    async def _fetch_binary(self, url):
        async with self.get(url) as response:
            return await response.read()

    async def get_excel(self):
        return await self._fetch_binary(self.url_excel)

    async def get_excel_fixed(self):
        return await self._fetch_binary(self.url_excel_fixed)

    async def get_excel_fixed_archive(self):
        return await self._fetch_binary(self.url_excel_fixed_archive)

    async def get_germany(self):
        async with self.get(self.url_germany) as response:
            result = await response.json()
        return result["features"][0]["attributes"]["Inz7T"]

    async def __aenter__(self) -> "Connector":
        self._session = aiohttp.ClientSession(raise_for_status=True)
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
        self._session = None


async def print_result_async(tasks: Iterable, column1_width: int = 20):
    date_string = None
    print_format = "{:" + str(column1_width) + "} {:>8}"
    for coro in asyncio.as_completed(tasks):
        city = await coro
        if date_string is None:
            date_string = city.updated[:10]
            print(f"Datum: {date_string}")
            print(print_format.format("Landkreis", "Inzidenz"))
        else:
            assert city.updated.startswith(date_string)
        print(print_format.format(city.city_name, f"{city.cases7_per_100k:3.2f}"))


def print_result(result: Iterable[CasesResult], print_id: bool = False):
    logging.debug("%s", str(result))
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


def print_table(headers: list[str], table: list[list[str]]):
    print_formats = []
    for i, header in enumerate(headers):
        size = max(len(x[i]) for x in table)
        size = max(size, len(header))
        if i == 0:  # First item left binding
            print_formats.append("{:" + str(size) + "}")
        else:  # all other right binding
            print_formats.append("{:>" + str(size) + "}")
    print_format = " ".join(print_formats)
    logging.debug("Format: '%s'", print_format)
    print(print_format.format(*headers))
    for row in table:
        print(print_format.format(*row))


async def handle_context_manager(con_needs_opening: bool, con: Connector, coro_func, *args, **kwargs):
    if con_needs_opening:
        async with con:
            return await coro_func(*args, **kwargs)
    return await coro_func(*args, **kwargs)


async def get_and_print_landkreise_tasks(con, landkreise):
    tasks = tuple(map(con.get_case, landkreise))
    await print_result_async(tasks)


async def main(landkreise: Optional[Iterable[Landkreise]] = None, keep_order: bool = False, con: Connector = None):
    con_needs_opening = False
    if con is None:
        con = Connector()
        con_needs_opening = True
    if landkreise is None:
        result = await handle_context_manager(con_needs_opening, con, con.get_all_cases)
        sort_by_name = lambda city: city.city_name
        result.sort(key=sort_by_name)
        print_result(result, True)
    elif keep_order:
        result = await handle_context_manager(con_needs_opening, con, con.get_cases, landkreise)
        print_result(result)
    else:
        await handle_context_manager(con_needs_opening, con, get_and_print_landkreise_tasks, con, landkreise)
    await asyncio.sleep(0.15)  # prevents "RuntimeError: Event loop is closed"


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

    PARSER = argparse.ArgumentParser(description="Corona Inzidenzzahlen")
    PARSER.add_argument(
        "-ids",
        "--region_ids",
        type=int,
        nargs="*",
        help="Region Ids für Regionen die geprüft werden sollen. Default verwendet im Skript hintelegte Ids. " "Es funktionieren nur bekannte ids.",
    )
    PARSER.add_argument("-a", "--all", action="store_true", help="Gibt alle Inzidenzzahlen inkl Region IDs aus. Ignoriert die anderen Parameter.")
    PARSER.add_argument("-o", "--force_order", action="store_true", help="Ausgabe ist in der selben Reihenfolge wie die IDs.")

    ARGS = PARSER.parse_args()

    if ARGS.region_ids is not None:
        REGIONS = Landkreise.find_by_ids(ARGS.region_ids)
    if ARGS.all:
        REGIONS = None

    asyncio.run(main(REGIONS, ARGS.force_order))
