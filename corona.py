import logging
from collections import namedtuple
from collections.abc import Iterable
import asyncio
import aiohttp # pip install aiohttp OPTIONAL: pip install aiodns

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
        self._session = None

    @staticmethod
    def parse_answer(response_json) -> CasesResult:
        region_id = response_json["features"][0]["attributes"]["OBJECTID"]
        bereich = response_json["features"][0]["attributes"]["GEN"]
        cases7_per_100k = response_json["features"][0]["attributes"]["cases7_per_100k"]
        last_update = response_json["features"][0]["attributes"]["last_update"]
        return CasesResult(bereich, cases7_per_100k, last_update, region_id)

    @staticmethod
    def parse_answer_all(response_json) -> list[CasesResult]:
        result = []
        for city in response_json["features"]:
            region_id = city["attributes"]["OBJECTID"]
            bereich = city["attributes"]["GEN"]
            cases7_per_100k = city["attributes"]["cases7_per_100k"]
            last_update = city["attributes"]["last_update"]
            result.append(CasesResult(bereich, cases7_per_100k, last_update, region_id))
        return result

    async def get_case(self, region_id):
        url = self.url.format(region_id)
        logging.info("Url: '%s'", url)
        async with self._session.get(url) as response:
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
        async with self._session.get(self.url_all) as response:
            response.raise_for_status()
            response_json = await response.json(content_type='text/plain')
        return self.parse_answer_all(response_json)

    async def __aenter__(self) -> "Connector":
        self._session = aiohttp.ClientSession()
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
        self._session = None


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
    if date_string == None:
        print("Keine Daten verfügbar")
    else:
        print("Datum: " + date_string)
        header = ["Landkreis", "Inzidenz"]
        print_table(header, to_print)

def print_table(headers: list[str], table:list[list[str]]):
    print_format = ""
    for i, header in enumerate(headers):
        size = max(len(x[i]) for x in table)
        size = max(size, len(header))
        if i == 0: # First item left binding
            print_format += '{:' + str(size) + '} '
        elif i + 1 == len(headers): # Last item right binding
            print_format += '{:>' + str(size) + '}'
        else: # all other items centered
            print_format += '{:^' + str(size) + '} '
    logging.debug("Format: '%s'", print_format)
    print(print_format.format(*headers))
    for row in table:
        print(print_format.format(*row))

async def main(region_ids=None):
    if region_ids is None:
        async with Connector() as con:
            result = await con.get_all_cases()
        sort_by_name = lambda city: city.city_name
        result.sort(key=sort_by_name)
        print_result(result, True)
    else:
        async with Connector() as con:
            result = await con.get_cases(region_ids)
        print_result(result)


if __name__ == "__main__":
    logging.basicConfig(
        # level=logging.DEBUG,
        format='%(asctime)s %(name)-22s %(levelname)-8s %(message)s',
    )

    REGION_IDS = (
        27,  # Hannover
        3,   # Lübeck
        16,  # Hamburg
        19,  # Wolfsburg
        87,  # Oberbergischer Kreis
        80,  # Köln
        413, # Berlin Mitte
    )
    asyncio.run(main(REGION_IDS))
