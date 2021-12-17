import os
from datetime import datetime
import unittest
import pandas as pd
from landkreise import DEUTSCHLAND, Landkreise
import corona_history


def get_testdata_file(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data", filename)


class TestLandkreise(unittest.TestCase):
    inzidenzen_result = [
        {
            "name": "SK Köln",
            datetime(2021, 6, 10): 20.2231347146,
            datetime(2021, 6, 9): 18.2927445827,
            datetime(2021, 6, 8): 23.7162216198,
            datetime(2021, 6, 7): 26.6577684874,
            datetime(2021, 6, 6): 27.5770018835,
            datetime(2021, 6, 5): 31.0700887888,
            datetime(2021, 6, 4): 32.8166322414,
        },
        {
            "name": "LK Nordfriesland",
            datetime(2021, 6, 10): 6.6284626185,
            datetime(2021, 6, 9): 10.2439876831,
            datetime(2021, 6, 8): 16.2698627908,
            datetime(2021, 6, 7): 21.090562877,
            datetime(2021, 6, 6): 22.8983254093,
            datetime(2021, 6, 5): 24.1035004309,
            datetime(2021, 6, 4): 27.7190254955,
        },
        {
            "name": "LK Oberbergischer Kreis",
            datetime(2021, 6, 10): 19.4812116579,
            datetime(2021, 6, 9): 26.4650422522,
            datetime(2021, 6, 8): 30.8758826275,
            datetime(2021, 6, 7): 31.6110226901,
            datetime(2021, 6, 6): 36.0218630655,
            datetime(2021, 6, 5): 39.329993347,
            datetime(2021, 6, 4): 43.0056936598,
        },
        {
            "name": "SK Wolfsburg",
            datetime(2021, 6, 10): 7.2364136334,
            datetime(2021, 6, 9): 14.4728272668,
            datetime(2021, 6, 8): 25.7294706965,
            datetime(2021, 6, 7): 32.1618383707,
            datetime(2021, 6, 6): 30.5537464521,
            datetime(2021, 6, 5): 28.9456545336,
            datetime(2021, 6, 4): 35.3780222077,
        },
    ]
    dates = [
        datetime(2021, 6, 4),
        datetime(2021, 6, 5),
        datetime(2021, 6, 6),
        datetime(2021, 6, 7),
        datetime(2021, 6, 8),
        datetime(2021, 6, 9),
        datetime(2021, 6, 10),
    ]
    germany_result = {
        datetime(2021, 6, 10): 29.677739690824133,
        datetime(2021, 6, 9): 26.2532926184853,
        datetime(2021, 6, 8): 24.71541768677133,
        datetime(2021, 6, 7): 24.289766611066298,
        datetime(2021, 6, 6): 22.920228262964493,
        datetime(2021, 6, 5): 20.764317588560164,
        datetime(2021, 6, 4): 19.255300356893997,
    }
    landkreise = (Landkreise.WOLFSBURG, Landkreise.OBERBERGISCHER_KREIS, Landkreise.KOELN, Landkreise.NORDFRIESLAND)
    header = ["Kreise", "04.06.", "05.06.", "06.06.", "07.06.", "08.06.", "09.06.", "10.06."]
    table = [
        ["Köln", "32.8", "31.1", "27.6", "26.7", "23.7", "18.3", "20.2"],
        ["Nordfriesland", "27.7", "24.1", "22.9", "21.1", "16.3", "10.2", "6.6"],
        ["Oberbergischer Kreis", "43.0", "39.3", "36.0", "31.6", "30.9", "26.5", "19.5"],
        ["Wolfsburg", "35.4", "28.9", "30.6", "32.2", "25.7", "14.5", "7.2"],
    ]
    graph_data = [
        [32.8166322414, 31.0700887888, 27.5770018835, 26.6577684874, 23.7162216198, 18.2927445827, 20.2231347146],
        [27.7190254955, 24.1035004309, 22.8983254093, 21.090562877, 16.2698627908, 10.2439876831, 6.6284626185],
        [43.0056936598, 39.329993347, 36.0218630655, 31.6110226901, 30.8758826275, 26.4650422522, 19.4812116579],
        [35.3780222077, 28.9456545336, 30.5537464521, 32.1618383707, 25.7294706965, 14.4728272668, 7.2364136334],
    ]
    kreis = ["Köln", "Nordfriesland", "Oberbergischer Kreis", "Wolfsburg"]
    x_axis_labels = ["04.06.", "05.06.", "06.06.", "07.06.", "08.06.", "09.06.", "10.06."]
    title = "7-Tages Inzidenzwerte, Stand: 10.06.2021"
    germany_inzidenzen = [
        29.677739690824133,
        26.2532926184853,
        24.71541768677133,
        24.289766611066298,
        22.920228262964493,
        20.764317588560164,
        19.255300356893997,
    ]

    def test_set_graph_title(self):
        title = corona_history.set_graph_title(self.dates[-1])
        self.assertEqual(self.title, title)

    def test_format_to_datetime(self):
        tests = (
            ("21.12.2021", datetime(2021, 12, 21)),
            ("21.1.2000", datetime(2000, 1, 21)),
            (datetime(2000, 1, 21), datetime(2000, 1, 21)),
            (44545, datetime(2021, 12, 15)),
            (44545.0, datetime(2021, 12, 15)),
            (44545.1, datetime(2021, 12, 15)),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.format_to_datetime(test[0]), test[1])

    def test_get_lines_inz(self):
        tests = (
            (None, []),
            ([], []),
            ([[], []], []),
            ([[1, 2, 3], [3, 4, 2], [2, 4, 0]], []),
            ([[1, 2, 3], [29.999, 4, 5], [5, 6, 7]], []),
            ([[1, 2, 3], [30.001, 4, 5], [5, 6, 7]], [35]),
            ([[1, 2, 3], [30.001, 46, 5], [5, 6, 7]], [35]),
            ([[1, 2, 3], [30.001, 46, 5], [85, 6, 7]], [35, 100]),
            ([[1, 2, 3], [30.001, 46, 5], [130, 6, 7]], [35, 100]),
            ([[1, 2, 3], [30.001, 46, 5], [190, 6, 7]], [35, 100, 200]),
            ([[1, 2, 300], [30.001, 46, 5], [190, 6, 7]], [35, 100, 200, 300]),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.get_lines_inz(pd.DataFrame(test[0])), test[1])

    def test_get_lines_hosp(self):
        tests = (
            (None, []),
            ([], []),
            ([[], []], []),
            ([[1, 1.2, 1.3], [1.3, 1.4, 1.2], [0.2, 0.4, 0]], []),
            ([[1, 2, 3], [3, 4, 2], [2, 4, 0]], [3]),
            ([[1, 2, 3], [3, 4, 5], [5, 5, 0]], [3, 6]),
            ([[1, 2, 3], [3, 4, 5], [5, 7, 0]], [3, 6]),
            ([[1, 2, 3], [3, 4, 5], [5, 8, 0]], [3, 6, 9]),
            ([[1, 2, 3], [3, 4, 5], [5, 12.9, 0]], [3, 6, 9]),
            ([[1, 2, 3], [3, 4, 5], [5, 13, 0]], [3, 6, 9, 15]),
            ([[1, 2, 3], [3, 4, 5], [5, 18, 0]], [3, 6, 9, 15, 20]),
            ([[1, 22.9, 3], [3, 4, 5], [5, 18, 0]], [3, 6, 9, 15, 20]),
            ([[1, 23, 3], [3, 4, 5], [5, 18, 0]], [3, 6, 9, 15, 20, 25]),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.get_lines_hosp(pd.DataFrame(test[0])), test[1])

    def test_excel_file(self):
        with open(get_testdata_file("Fallzahlen_Inzidenz_aktualisiert.xlsx"), "br") as excel_file:
            excel = excel_file.read()
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
        result = corona_history.read_excel(excel, landkreise, False, 8)
        expected_result = (
            pd.DataFrame(
                [
                    [141.972258, 127.249209, 139.343142, 134.610733, 133.559087, 124.620093, 138.817319, 120.413507],
                    [402.850118, 378.556307, 356.932146, 357.733040, 357.733040, 338.511564, 333.439229, 279.512308],
                    [250.313364, 255.063758, 257.546918, 260.947768, 266.615852, 269.152994, 279.895362, 235.954219],
                    [222.274155, 236.209568, 227.467477, 227.813698, 228.159920, 224.784261, 196.999991, 198.125211],
                    [555.977030, 543.332798, 548.778124, 502.723586, 450.485372, 388.187149, 329.580673, 268.666855],
                    [228.866877, 226.550411, 232.573224, 251.104954, 251.104954, 249.715075, 270.563272, 242.765676],
                    [101.108605, 96.920675, 98.715502, 105.894811, 111.279293, 114.868948, 119.655154, 119.655154],
                    [479.942878, 477.734552, 443.505497, 417.005583, 421.054181, 397.498703, 397.130648, 328.672538],
                    [146.907741, 154.848700, 148.892981, 148.892981, 148.892981, 137.477852, 138.470472, 147.404051],
                    [247.900517, 247.900517, 234.980620, 230.135659, 213.178295, 222.060724, 225.290698, 230.943152],
                    [451.081547, 438.472568, 424.541962, 414.997139, 405.731314, 391.340122, 375.753573, 340.126143],
                ],
                index=(
                    Landkreise.AURICH,
                    Landkreise.BERLIN_MITTE,
                    Landkreise.HAMBURG,
                    Landkreise.HANNOVER,
                    Landkreise.KOELN,
                    Landkreise.LUEBECK,
                    Landkreise.NORDFRIESLAND,
                    Landkreise.OBERBERGISCHER_KREIS,
                    Landkreise.OSTHOLSTEIN,
                    Landkreise.WOLFSBURG,
                    DEUTSCHLAND,
                ),
                columns=(
                    datetime(2021, 12, 9),
                    datetime(2021, 12, 10),
                    datetime(2021, 12, 11),
                    datetime(2021, 12, 12),
                    datetime(2021, 12, 13),
                    datetime(2021, 12, 14),
                    datetime(2021, 12, 15),
                    datetime(2021, 12, 16),
                ),
            ),
            pd.DataFrame(
                [
                    [5.813179, 6.167974, 5.785887, 5.813179, 5.758595, 5.540260, 5.704011, 4.803378],
                    [6.639755, 5.937992, 5.991974, 5.884010, 5.506138, 5.290211, 4.750394, 3.616777],
                    [4.360635, 4.073258, 4.160721, 4.160721, 3.910828, 3.685924, 3.386052, 2.986223],
                    [8.022060, 7.642714, 7.291260, 6.917493, 6.571618, 5.511680, 4.875717, 3.966401],
                    [5.050028, 4.775196, 4.603427, 4.500365, 4.225534, 3.881994, 3.469747, 3.435393],
                    [9.647041, 9.104681, 8.513015, 8.152243, 7.732545, 7.002583, 6.232936, 5.172267],
                ],
                index=("Berlin", "Hamburg", "Niedersachsen", "Nordrhein-Westfalen", "Schleswig-Holstein", DEUTSCHLAND),
                columns=(
                    datetime(2021, 12, 9),
                    datetime(2021, 12, 10),
                    datetime(2021, 12, 11),
                    datetime(2021, 12, 12),
                    datetime(2021, 12, 13),
                    datetime(2021, 12, 14),
                    datetime(2021, 12, 15),
                    datetime(2021, 12, 16),
                ),
            ),
        )
        pd.testing.assert_frame_equal(result[0], expected_result[0], atol=0.0001)  # expected result has less decimal places
        pd.testing.assert_frame_equal(result[1], expected_result[1], atol=0.0001)  # expected result has less decimal places

    def test_excel_file_fixed(self):
        with open(get_testdata_file("Fallzahlen_Kum_Tab.xlsx"), "br") as excel_file:
            excel = excel_file.read()
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
        result = corona_history.read_excel(excel, landkreise, True, 8)
        expected_result = pd.DataFrame(
            (
                [176.150764, 166.160124, 139.868965, 130.929971, 123.568446, 125.145916, 108.845397, 107.793751],
                [301.136470, 242.404180, 361.737515, 396.976889, 372.950043, 345.719617, 345.719617, 344.918723],
                [224.510089, 217.924315, 211.068633, 194.172346, 207.559820, 216.736717, 225.913614, 231.581698],
                [218.725386, 207.126968, 200.115984, 200.635316, 207.386634, 217.686722, 188.171345, 179.948586],
                [415.229193, 403.692485, 391.140547, 392.340364, 380.526775, 368.067131, 340.009857, 338.071690],
                [188.097069, 194.119882, 191.803415, 222.380771, 226.550411, 225.623824, 251.104954, 251.104954],
                [111.877569, 97.518950, 87.946538, 93.929296, 87.946538, 90.937917, 95.125847, 102.903432],
                [429.151377, 446.081877, 443.137443, 429.151377, 373.943224, 420.318073, 402.283409, 409.276442],
                [132.514753, 143.433571, 146.907741, 146.907741, 154.848700, 148.892981, 148.892981, 148.892981],
                [230.135659, 264.857881, 264.050388, 246.285530, 248.708010, 234.173127, 222.868217, 178.456072],
                [441.863824, 432.239632, 426.957931, 422.281125, 413.703171, 402.940142, 390.912006, 389.155047],
            ),
            index=(
                Landkreise.AURICH,
                Landkreise.BERLIN_MITTE,
                Landkreise.HAMBURG,
                Landkreise.HANNOVER,
                Landkreise.KOELN,
                Landkreise.LUEBECK,
                Landkreise.NORDFRIESLAND,
                Landkreise.OBERBERGISCHER_KREIS,
                Landkreise.OSTHOLSTEIN,
                Landkreise.WOLFSBURG,
                DEUTSCHLAND,
            ),
            columns=(
                datetime(2021, 12, 6),
                datetime(2021, 12, 7),
                datetime(2021, 12, 8),
                datetime(2021, 12, 9),
                datetime(2021, 12, 10),
                datetime(2021, 12, 11),
                datetime(2021, 12, 12),
                datetime(2021, 12, 13),
            ),
        )
        pd.testing.assert_frame_equal(result[0], expected_result, atol=0.0001)  # expected result has less decimal places
        self.assertIsNone(result[1])


if __name__ == "__main__":
    unittest.main()
