from functools import lru_cache
from io import StringIO
import json
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, NonCallableMock

from corona import CasesResult, Connector, main
from landkreise import Landkreise


def get_testdata_file(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data", filename)


def create_answer(value: str = None, json_object=None):
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
    prefix = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID="
    suffix = "&outFields=OBJECTID,GEN,county,cases7_per_100k,last_update&returnGeometry=false&outSR=&f=json"
    url = url if not url.startswith(prefix) else url[len(prefix) :]
    city_id = url if not url.endswith(suffix) else url[: -len(suffix)]
    with open(get_testdata_file(city_id + ".json"), encoding="utf-8") as f:
        result = f.read()
    return create_answer(json_object=json.loads(result))


class TestCorona(unittest.IsolatedAsyncioTestCase):
    landkreise = (
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
    ordered_result = """Datum: 27.04.2022
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
        with open(get_testdata_file("de.json")) as f:
            result = f.read()
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
            CasesResult("Oberbergischer Kreis", "LK Oberbergischer Kreis", 778.803013629053, "27.04.2022, 00:00 Uhr", 87),
            CasesResult("Köln", "SK Köln", 553.485101033874, "27.04.2022, 00:00 Uhr", 80),
            CasesResult("Ostholstein", "LK Ostholstein", 1891.4371646806, "27.04.2022, 00:00 Uhr", 8),
        ]
        self.con._session.get = MagicMock(side_effect=get_city)
        result = await self.con.get_cases(self.landkreise)
        self.assertEqual(result, expected_result)

    async def test_main_ordered(self):
        self.con._session.get = MagicMock(side_effect=get_city)
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        try:
            await main(self.landkreise, keep_order=True, con=self.con)
        finally:
            sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), self.ordered_result)

    async def test_main_unordered(self):
        self.con._session.get = MagicMock(side_effect=get_city)
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        try:
            await main(self.landkreise, keep_order=False, con=self.con)
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
