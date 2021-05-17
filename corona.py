import logging
import json
import asyncio
import aiohttp # pip install aiohttp OPTIONAL: pip install aiodns

class Connector:

    def __init__(self):
        fields = (
            # 'OBJECTID',
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

        self.url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID={}&outFields=" + fieldstr + "&returnGeometry=false&outSR=&f=json"

    def parse_answer(self, response_json):
        bereich = response_json["features"][0]["attributes"]["GEN"]
        cases7_per_100k = response_json["features"][0]["attributes"]["cases7_per_100k"]
        last_update = response_json["features"][0]["attributes"]["last_update"]
        return bereich, cases7_per_100k, last_update

    async def get_case(self, region_id, session):
        url = self.url.format(region_id)
        logging.info("Url: '%s'", url)
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()
        logging.debug("%i loaded", region_id)
        response_json = json.loads(text)
        return self.parse_answer(response_json)

    async def get_cases(self, region_ids):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for region_id in region_ids:
                tasks.append(self.get_case(region_id, session))
            return await asyncio.gather(*tasks)


def print_result(result):
    date_string = result[0][2][0:10]
    print("Datum: " + date_string)
    for city in result:
        print(f"{city[0]}: {city[1]:3.2f}")
        assert city[2].startswith(date_string)

async def main(region_ids):
    con = Connector()
    result = await con.get_cases(region_ids)
    print_result(result)


if __name__ == "__main__":
    logging.basicConfig(
        # level=logging.DEBUG,
        format='%(asctime)s %(name)-22s %(levelname)-8s %(message)s',
    )
    
    region_ids = (
        27, # Hannover
        3,  # Lübeck 
        16, # Hamburg
        19, # Wolfsburg
        87, # Oberbergischer Kreis
        80, # Köln
        413, # Berlin Mitte
    )
    asyncio.run(main(region_ids))
