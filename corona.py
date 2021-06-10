import os
import logging
from collections import namedtuple
from typing import Iterable, List
import argparse
import asyncio
import aiohttp # pip install aiohttp OPTIONAL: pip install aiodns
from landkreise import Landkreise

CasesResult = namedtuple('CasesResult', ('city_name', 'cases7_per_100k', 'updated', 'region_id'))

class Connector:

    def __init__(self):
        fields = (
            'OBJECTID',
            'GEN',
            # 'BEZ',
            # 'BL',
            # 'cases',
            # 'deaths',
            # 'cases_per_population',

            'cases7_per_100k',
            # 'cases7_lk',
            # 'death7_lk',
            # 'cases7_bl_per_100k',
            # 'cases7_bl',
            # 'death7_bl',

            'last_update'
        )
        fieldstr = ",".join(fields)

        self.url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/"\
            "RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID={}&outFields="\
             + fieldstr + "&returnGeometry=false&outSR=&f=json"

        self.url_all = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/"\
            "RKI_Landkreisdaten/FeatureServer/0/query?where=1=1&outFields="\
             + fieldstr + "&returnGeometry=false&outSR=&f=json"
        self.url_excel = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/"\
            "Fallzahlen_Kum_Tab.xlsx?__blob=publicationFile"
        self._session = None
        self.set_proxy()

    def set_proxy(self):
        try:
            self.proxy = os.environ['HTTP_PROXY']
        except KeyError:
            self.proxy = None
            logging.info("Not using Proxy.")

    @classmethod
    def parse_answer(cls, response_json) -> CasesResult:
        results = cls.parse_answer_all(response_json)
        assert len(results) == 1
        return results[0]

    @staticmethod
    def parse_answer_all(response_json) -> List[CasesResult]:
        result = []
        for city in response_json["features"]:
            region_id = city["attributes"]["OBJECTID"]
            bereich = city["attributes"]["GEN"]
            cases7_per_100k = city["attributes"]["cases7_per_100k"]
            last_update = city["attributes"]["last_update"]
            result.append(CasesResult(bereich, cases7_per_100k, last_update, region_id))
        return result

    def get(self, url):
        return self._session.get(url, proxy=self.proxy)

    async def get_case(self, region_id):
        url = self.url.format(region_id)
        logging.info("Url: '%s'", url)
        async with self.get(url) as response:
            response.raise_for_status()
            response_json = await response.json(content_type='text/plain')
        logging.debug("%i loaded", region_id)
        return self.parse_answer(response_json)

    async def get_cases(self, region_ids):
        tasks = []
        for region_id in region_ids:
            tasks.append(self.get_case(region_id))
        return await asyncio.gather(*tasks)

    async def get_all_cases(self):
        async with self.get(self.url_all) as response:
            response.raise_for_status()
            response_json = await response.json(content_type='text/plain')
        return self.parse_answer_all(response_json)

    async def get_excel(self):
        async with self.get(self.url_excel) as response:
            response.raise_for_status()
            result = await response.read()
        return result

    async def __aenter__(self) -> "Connector":
        self._session = aiohttp.ClientSession()
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
        self._session = None


async def print_result_async(tasks, column1_width=20):
    date_string = None
    print_format = "{:" + str(column1_width) + "} {:>8}"
    for coro in asyncio.as_completed(tasks):
        city = await coro
        if date_string is None:
            date_string = city.updated[0:10]
            print("Datum: " + date_string)
            print(print_format.format("Kreis", "Inzidenz"))
        else:
            assert city.updated.startswith(date_string)
        print(print_format.format(city.city_name, f"{city.cases7_per_100k:3.2f}"))


def print_result(result: Iterable[CasesResult], print_id: bool = False):
    to_print = []
    date_string = None
    for city in result:
        if date_string is None:
            date_string = city.updated[0:10]
        else:
            assert city.updated.startswith(date_string)
        temp = []
        if print_id:
            temp.append(city.city_name + f" ({city.region_id})")
        else:
            temp.append(city.city_name)
        temp.append(f"{city.cases7_per_100k:3.2f}")
        to_print.append(temp)
    if date_string is None:
        print("Keine Daten verfügbar")
    else:
        print("Datum: " + date_string)
        header = ["Landkreis", "Inzidenz"]
        print_table(header, to_print)

def print_table(headers: List[str], table: List[List[str]]):
    print_formats = []
    for i, header in enumerate(headers):
        size = max(len(x[i]) for x in table)
        size = max(size, len(header))
        if i == 0: # First item left binding
            print_formats.append('{:' + str(size) + '}')
        else: # all other right binding
            print_formats.append('{:>' + str(size) + '}')
    print_format = " ".join(print_formats)
    logging.debug("Format: '%s'", print_format)
    print(print_format.format(*headers))
    for row in table:
        print(print_format.format(*row))

async def main(region_ids=None, keep_order=False):
    if region_ids is None:
        async with Connector() as con:
            result = await con.get_all_cases()
        sort_by_name = lambda city: city.city_name
        result.sort(key=sort_by_name)
        print_result(result, True)
    elif keep_order:
        async with Connector() as con:
            result = await con.get_cases(region_ids)
        print_result(result)
    else:
        async with Connector() as con:
            tasks = []
            for region_id in region_ids:
                tasks.append(con.get_case(region_id))
            await print_result_async(tasks)



if __name__ == "__main__":
    logging.basicConfig(
        # level=logging.DEBUG,
        format='%(asctime)s %(name)-22s %(levelname)-8s %(message)s',
    )

    REGIONS_DEFAULT = (
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

    REGION_IDS_DEFAULT = tuple(lk.id for lk in REGIONS_DEFAULT)
    PARSER = argparse.ArgumentParser(description='Corona Inzidenzzahlen')
    PARSER.add_argument("-ids", '--region_ids', type=int, nargs='*', default=REGION_IDS_DEFAULT,
                        help='Region Ids für Regionen die geprüft werden sollen. Default verwendet im Skript hintelegte Ids.')
    PARSER.add_argument("-a", '--all', action='store_true',
                        help='Gibt alle Inzidenzzahlen inkl Region IDs aus. Ignoriert die anderen Parameter.')
    PARSER.add_argument("-o", '--force_order', action='store_true',
                        help='Ausgabe ist in der selben Reihenfolge wie die IDs.')

    ARGS = PARSER.parse_args()
    ALL = ARGS.all
    FORCE_ORDER = ARGS.force_order
    REGION_IDS = ARGS.region_ids
    if ALL:
        REGION_IDS = None

    asyncio.run(main(REGION_IDS, FORCE_ORDER))
