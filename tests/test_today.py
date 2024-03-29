import json
import sys
import unittest
from functools import lru_cache
from io import StringIO
from typing import Optional
from unittest.mock import AsyncMock, MagicMock, NonCallableMock

from corona.landkreise import Landkreise
from corona.rki_connector import CasesResult, Connector
from corona.today import today

from .testing_utils import get_testdata_text


def create_answer(value: Optional[str] = None, json_object=None):
    if value is None and json_object is None:
        raise ValueError("either value or json_object must not be 'None'!")
    result = NonCallableMock()
    result.__aenter__ = AsyncMock(return_value=result)
    result.__aexit__ = AsyncMock()
    if value is None:
        value = json.dumps(json_object)
    result.text = AsyncMock(return_value=value)
    if json_object is not None:
        result.json = AsyncMock(return_value=json_object)
    return result


@lru_cache(maxsize=32)
def get_city(url: str, *args, **kwargs):
    prefix = (
        "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/"
        "query?where=OBJECTID="
    )
    suffix = "&outFields=OBJECTID,GEN,county,cases7_per_100k,last_update&returnGeometry=false&outSR=&f=json"
    url = url.removeprefix(prefix)
    city_id = url.removesuffix(suffix)
    result = get_testdata_text(f"{city_id}.json")
    return create_answer(json_object=json.loads(result))


class TestCorona(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.landkreise = (
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
        cls.landkreise_ids = tuple(lk.id for lk in cls.landkreise)
        cls.ordered_result = """Datum: 27.04.2022
Landkreis            Inzidenz
Berlin Mitte           498.16
Region Hannover        880.87
Aurich                1843.54
Nordfriesland         1680.56
Lübeck                1317.14
Hamburg                909.43
Wolfsburg             1337.21
Oberbergischer Kreis   778.80
Köln                   553.49
Ostholstein           1891.44
"""

    def setUp(self):
        self.con = Connector()
        self.con._session = NonCallableMock()

    async def test_corona_germany_live(self):
        async with Connector() as con:
            result = await con.get_germany()
            self.assertIsInstance(result, (float, int))
            # self.assertEqual(result, 702.1)  # enable line and put the real result of the current day for testing

    async def test_corona_germany_mock(self):
        result = get_testdata_text("de.json")
        self.con._session.get = MagicMock(return_value=create_answer(json_object=json.loads(result)))
        result = await self.con.get_germany()
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 702.1)

    async def test_get_cases(self):
        expected_result = [
            CasesResult("Berlin Mitte", "SK Berlin Mitte", 498.156606982201, "27.04.2022, 00:00 Uhr", 413),
            CasesResult("Region Hannover", "Region Hannover", 880.873862879004, "27.04.2022, 00:00 Uhr", 27),
            CasesResult("Aurich", "LK Aurich", 1843.53605569519, "27.04.2022, 00:00 Uhr", 51),
            CasesResult("Nordfriesland", "LK Nordfriesland", 1680.55663577569, "27.04.2022, 00:00 Uhr", 7),
            CasesResult("Lübeck", "SK Lübeck", 1317.14277772115, "27.04.2022, 00:00 Uhr", 3),
            CasesResult("Hamburg", "SK Hamburg", 909.430503358205, "27.04.2022, 00:00 Uhr", 16),
            CasesResult("Wolfsburg", "SK Wolfsburg", 1337.20930232558, "27.04.2022, 00:00 Uhr", 19),
            CasesResult(
                "Oberbergischer Kreis", "LK Oberbergischer Kreis", 778.803013629053, "27.04.2022, 00:00 Uhr", 87
            ),
            CasesResult("Köln", "SK Köln", 553.485101033874, "27.04.2022, 00:00 Uhr", 80),
            CasesResult("Ostholstein", "LK Ostholstein", 1891.4371646806, "27.04.2022, 00:00 Uhr", 8),
        ]
        self.con._session.get = MagicMock(side_effect=get_city)
        generator = self.con.get_cases(self.landkreise, True)
        result = [x async for x in generator]
        self.assertEqual(result, expected_result)

    async def test_today_ordered(self):
        self.con._session.get = MagicMock(side_effect=get_city)
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        try:
            await today(self.landkreise_ids, keep_order=True, con=self.con)
        finally:
            sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), self.ordered_result)

    async def test_today_unordered(self):
        self.con._session.get = MagicMock(side_effect=get_city)
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        try:
            await today(self.landkreise_ids, keep_order=False, con=self.con)
        finally:
            sys.stdout = sys.__stdout__
        result_list = capturedOutput.getvalue().split("\n")
        expected_list = self.ordered_result.split("\n")
        # first two lines should match
        self.assertEqual(result_list[0], expected_list[0])
        self.assertEqual(result_list[1], expected_list[1])
        # first line should be empty
        self.assertEqual(result_list[-1], "")
        # length should be equal
        self.assertEqual(len(result_list), len(expected_list))
        # the rest should match unordered
        self.assertEqual(set(result_list), set(expected_list))


if __name__ == "__main__":
    unittest.main()
