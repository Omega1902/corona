import asyncio
import logging
import os
from collections import namedtuple
from collections.abc import AsyncIterable, Iterable

import aiohttp  # pip install aiohttp OPTIONAL: pip install aiodns

from corona.landkreise import Landkreise

LOG = logging.getLogger(__name__)
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
            f"RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID={{}}&outFields={fieldstr}"
            "&returnGeometry=false&outSR=&f=json"
        )
        self.url_all = (
            "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/"
            f"RKI_Landkreisdaten/FeatureServer/0/query?where=1=1&outFields={fieldstr}"
            "&returnGeometry=false&outSR=&f=json"
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
        if self._session is None:
            raise RuntimeError("Context was never opend")
        return self._session.get(url, proxy=self.proxy)

    async def get_case(self, landkreis: Landkreise) -> CasesResult:
        url = self.url.format(landkreis.id)
        LOG.info("Url: '%s'", url)
        async with self.get(url) as response:
            response_json = await response.json(encoding="utf-8")
        LOG.debug("%i loaded", landkreis.id)
        response = self.parse_answer(response_json)
        if response.county != landkreis.lk_name:
            raise RuntimeError(f"Wrong lk_name was returned: requested {landkreis.lk_name}, returned {response.county}")
        if response.region_id != landkreis.id:
            raise RuntimeError(f"Wrong id was returned: requested {landkreis.id}, returned {response.region_id}")
        return response

    async def get_cases(
        self, landkreise: Iterable[Landkreise], force_order: bool = False
    ) -> AsyncIterable[CasesResult]:
        tasks = tuple(map(asyncio.create_task, map(self.get_case, landkreise)))
        if not force_order:
            tasks = asyncio.as_completed(tasks)
        for task in tasks:
            yield await task

    async def get_all_cases(self):
        async with self.get(self.url_all) as response:
            response_json = await response.json()
        LOG.debug("Loaded: %s", str(response_json))
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
        if self._session is None:
            raise RuntimeError("__aexit__ called without __aenter__ before")
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
        self._session = None
