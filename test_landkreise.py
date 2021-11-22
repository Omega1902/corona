import unittest
from typing import Iterable
import asyncio
from corona import Connector
from landkreise import Landkreise

async def test_be(landkreise: Iterable[Landkreise]):
    """ tests consistency to BE, should run without an exception """
    async with Connector() as con:
        tasks = [con.get_case(landkreis) for landkreis in landkreise]
        await asyncio.gather(*tasks)

class TestLandkreise(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.landkreise_dict = [lk for lk in Landkreise]

    def test_uniqueness(self):
        for landkreis in Landkreise:
            same_id = [lk for lk in Landkreise if lk.id == landkreis.id]
            self.assertEqual(len(same_id), 1, "All Lankreise should have an unique id")
            same_lk_name = [lk for lk in Landkreise if lk.lk_name == landkreis.lk_name]
            self.assertEqual(len(same_lk_name), 1, "All Lankreise should have an unique lk name")

    def test_if_value_is_id(self):
        self.assertEqual(Landkreise.KOELN.value, 80)
        self.assertEqual(Landkreise.HANNOVER.value, 27)

    def test_find_by_id(self):
        for landkreis in Landkreise:
            self.assertEqual(Landkreise.find_by_id(landkreis.value), landkreis)

        self.assertIsNone(Landkreise.find_by_id(-1))

    def test_find_by_ids(self):
        tests = [{
                "test":     [lk.id for lk in Landkreise] + [-1],
                "expect":   self.landkreise_dict
            }, {
                "test":     (lk.id for lk in Landkreise),
                "expect":   self.landkreise_dict
            }, {"test": tuple((-1, -2)), "expect": []}]
        for test in tests:
            with self.subTest(test=test):
                landkreise = Landkreise.find_by_ids(test["test"])
                self.assertEqual(landkreise, test["expect"])

    def test_find_by_lk_name(self):
        for landkreis in Landkreise:
            self.assertEqual(Landkreise.find_by_lk_name(landkreis.lk_name), landkreis)

        self.assertIsNone(Landkreise.find_by_lk_name("DOES NOT EXIST"))

    def test_find_by_lk_names(self):
        tests = [{
                "test":     [lk.lk_name for lk in Landkreise] + ["DOES NOT EXIST"],
                "expect":   self.landkreise_dict
            }, {
                "test":     (lk.lk_name for lk in Landkreise),
                "expect":   self.landkreise_dict
            }, {"test": tuple(("DOES NOT EXIST", "DOES NOT EXIST2")), "expect": []}]
        for test in tests:
            with self.subTest(test=test):
                landkreise = Landkreise.find_by_lk_names(test["test"])
                self.assertEqual(landkreise, test["expect"])

    def test_name(self):
        tests = {
            "Aurich":       Landkreise.AURICH,
            "Berlin Mitte": Landkreise.BERLIN_MITTE,
            "Köln":         Landkreise.KOELN,
            "Hannover":     Landkreise.HANNOVER,
            "Wolfsburg":    Landkreise.WOLFSBURG,
        }
        for name, landkreis in tests.items():
            self.assertEqual(name, landkreis.name)

    def test_consistency_be(self):
        """ This testcase should check whether the Landkreis values are matching the ones of the BE """
        asyncio.run(test_be(self.landkreise_dict))

if __name__ == '__main__':
    unittest.main()
