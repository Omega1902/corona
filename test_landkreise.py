import unittest
from landkreise import Landkreise

class TestLandkreise(unittest.TestCase):

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

    def test_find_by_lk_name(self):
        for landkreis in Landkreise:
            self.assertEqual(Landkreise.find_by_lk_name(landkreis.lk_name), landkreis)

        self.assertIsNone(Landkreise.find_by_lk_name("DOES NOT EXIST"))

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

if __name__ == '__main__':
    unittest.main()
