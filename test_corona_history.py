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

    def test_dataframe_max(self):
        tests = (
            (None, 0),
            ([], 0),
            ([[], []], 0),
            ([[1, 2, 3], [3, 4, 2], [2, 4, 0]], 4),
            ([[1, 2, 3], [29.999, 4, 5], [5, 6, 7]], 29.999),
            ([[1, 2, 3], [30.001, 4, 5], [5, 6, 7]], 30.001),
            ([[1, 2, 3], [30.001, 46, 5], [5, 6, 7]], 46),
            ([[1, 2, 3], [30.001, 46, 5], [85, 6, 7]], 85),
            ([[1, 2, 3], [30.001, 46, 5], [130, 6, 7]], 130),
            ([[1, 2, 3], [30.001, 46, 5], [190, 6, 7]], 190),
            ([[1, 2, 300], [30.001, 46, 5], [190, 6, 7]], 300),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.dataframe_max(pd.DataFrame(test[0])), test[1])

    def test_get_lines_inz(self):
        tests = (
            (0, []),
            (29.999, []),
            (30.001, [35]),
            (46, [35]),
            (85, [35, 100]),
            (130, [35, 100]),
            (190, [35, 100, 200]),
            (300, [35, 100, 200, 300]),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.get_lines_inz(test[0]), test[1])

    def test_get_lines_hosp(self):
        tests = (
            (0, []),
            (1.4, []),
            (3, [3]),
            (5, [3, 6]),
            (7.999, [3, 6]),
            (8, [3, 6, 9]),
            (12.9, [3, 6, 9]),
            (13, [3, 6, 9, 15]),
            (18, [3, 6, 9, 15, 20]),
            (22.9, [3, 6, 9, 15, 20]),
            (23, [3, 6, 9, 15, 20, 25]),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.get_lines_hosp(test[0]), test[1])

    def test_get_bg_colors(self):
        tests = (
            ((1.4, tuple(), 8), [([-0.5, 8.5], [0, 0], [1.4, 1.4], "#00ff00")]),
            ((3, (3,), 8), [([-0.5, 8.5], [0, 0], [3, 3], "#00ff00")]),
            ((4.9, (3,), 8), [([-0.5, 8.5], [0, 0], [3, 3], "#00ff00"), ([-0.5, 8.5], [3, 3], [4.9, 4.9], "#ffff00")]),
            ((5, (3, 6), 8), [([-0.5, 8.5], [0, 0], [3, 3], "#00ff00"), ([-0.5, 8.5], [3, 3], [6, 6], "#ffff00")]),
            (
                (23, (3, 6, 9, 15, 20, 25), 8),
                [
                    ([-0.5, 8.5], [0, 0], [3, 3], "#00ff00"),
                    ([-0.5, 8.5], [3, 3], [6, 6], "#ffff00"),
                    ([-0.5, 8.5], [6, 6], [9, 9], "#ffa500"),
                    ([-0.5, 8.5], [9, 9], [25, 25], "#ff0000"),
                ],
            ),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.get_bg_colors(*test[0]), test[1])

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
        with open(get_testdata_file("Fallzahlen_Kum_Tab_aktuell.xlsx"), "br") as excel_file:
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
        index_expected = (
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
        )
        columns_expected = (
            datetime(2022, 2, 7),
            datetime(2022, 2, 8),
            datetime(2022, 2, 9),
            datetime(2022, 2, 10),
            datetime(2022, 2, 11),
            datetime(2022, 2, 12),
            datetime(2022, 2, 13),
            datetime(2022, 2, 14),
        )
        result = corona_history.read_excel(excel, landkreise, True, 8)
        expected_result1 = pd.DataFrame(
            (
                (830.274795, 961.204766, 799.251228, 878.124704, 953.843242, 1073.730926, 1036.397480, 1092.660560),
                (1896.519044, 1657.318444, 1650.377355, 1533.179739, 1344.702481, 1151.953783, 1148.483239, 1147.682344),
                (1526.279934, 1405.360819, 1298.962795, 1226.843180, 1205.574371, 1210.864582, 1292.538967, 1232.619227),
                (1484.251253, 1473.431833, 1491.262237, 1537.223131, 1481.568037, 1561.285520, 1510.650637, 1488.579021),
                (1830.737113, 1810.247919, 1770.930819, 1767.423659, 1677.621925, 1658.240255, 1655.932914, 1621.322790),
                (1101.711405, 1084.569554, 1095.688593, 1049.359265, 1058.161838, 1018.318616, 1045.652919, 1014.612270),
                (691.008513, 662.889552, 675.453343, 608.446457, 585.711978, 540.243020, 460.672342, 564.772326),
                (1649.987670, 1829.230141, 1695.258356, 1668.390388, 1675.383421, 1758.931759, 1710.348584, 1765.556737),
                (586.638344, 585.149414, 652.151255, 686.892951, 668.033173, 634.284098, 633.787788, 633.787788),
                (1226.582687, 1384.851421, 1414.728682, 1589.147287, 1563.307494, 1658.591731, 1673.934109, 1717.538760),
                (1426.008728, 1440.997599, 1450.774518, 1465.382173, 1472.199559, 1474.323303, 1466.545061, 1459.807044),
            ),
            index=index_expected,
            columns=columns_expected,
        )
        expected_result2 = pd.DataFrame(
            (
                (3.547950, 4.066496, 4.557751, 4.994422, 4.121080, 4.475875, 4.421291, 4.393999),
                (5.830029, 3.724741, 3.670759, 4.588449, 4.318540, 2.968996, 3.508814, 2.861033),
                (4.385625, 4.485582, 4.573044, 4.835432, 4.585539, 4.473087, 4.510571, 4.398119),
                (5.383371, 5.662303, 6.181114, 6.398681, 6.789184, 7.040222, 6.660876, 6.354052),
                (5.530983, 5.153090, 5.153090, 5.256152, 6.046292, 6.149354, 5.668399, 5.324859),
                (5.409174, 5.602788, 6.068184, 6.226923, 6.463830, 6.457817, 6.230531, 5.932293),
            ),
            index=("Berlin", "Hamburg", "Niedersachsen", "Nordrhein-Westfalen", "Schleswig-Holstein", DEUTSCHLAND),
            columns=columns_expected,
        )
        pd.testing.assert_frame_equal(result[0], expected_result1, atol=0.0001)  # expected result has less decimal places
        pd.testing.assert_frame_equal(result[1], expected_result2, atol=0.0001)  # expected result has less decimal places

    def test_excel_file_fixed_archive(self):
        with open(get_testdata_file("Fallzahlen_Kum_Tab_Archiv.xlsx"), "br") as excel_file:
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
        result = corona_history.read_excel(excel, landkreise, True, 8, True)
        expected_result = pd.DataFrame(
            (
                (44.732918, 44.169147, 47.849909, 48.416806, 38.943952, 34.733795, 35.260065, 35.260065),
                (111.526147, 116.930651, 116.930651, 116.862327, 120.330843, 109.391676, 114.194237, 121.664888),
                (79.049618, 77.679735, 80.162895, 81.156887, 79.860106, 78.995585, 80.346399, 78.131065),
                (91.095876, 70.975392, 98.326885, 100.092999, 99.833467, 90.144257, 101.390661, 112.464044),
                (136.872288, 131.333883, 121.089287, 123.231145, 116.502743, 112.355097, 113.829816, 115.120194),
                (78.676750, 73.663631, 67.177525, 67.106639, 72.197488, 65.255422, 61.090182, 59.238964),
                (30.585013, 29.913788, 34.101719, 32.384132, 33.583544, 32.983838, 27.586483, 27.586483),
                (155.618642, 156.791155, 161.943916, 153.779178, 153.043393, 155.986535, 145.317645, 143.846074),
                (27.837014, 27.297046, 29.778596, 31.316641, 29.825372, 30.322462, 29.328283, 30.322462),
                (113.694090, 105.781654, 124.354005, 124.982865, 114.500431, 107.243362, 109.662385, 106.437021),
                (80.195990, 80.679424, 83.111027, 84.255876, 83.820545, 82.658859, 83.527117, 83.785670),
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
                datetime(2021, 9, 3),
                datetime(2021, 9, 4),
                datetime(2021, 9, 5),
                datetime(2021, 9, 6),
                datetime(2021, 9, 7),
                datetime(2021, 9, 8),
                datetime(2021, 9, 9),
                datetime(2021, 9, 10),
            ),
        )
        pd.testing.assert_frame_equal(result[0], expected_result, atol=0.0001)  # expected result has less decimal places
        self.assertIsNone(result[1])

    def test_format_to_week(self):
        tests = (
            (datetime(2020, 12, 26), "2020-52"),
            (datetime(2020, 12, 31), "2020-53"),
            (datetime(2021, 1, 3), "2020-53"),
            (datetime(2021, 1, 4), "2021-01"),
            (datetime(2021, 12, 31), "2021-52"),
            (datetime(2022, 1, 2), "2021-52"),
            (datetime(2022, 1, 3), "2022-01"),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.format_to_week(test[0]), test[1])

    def test_get_colors_integrety(self):
        """Tests if the method returns usable responses - not if the color values are correct"""
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
        df1, df2 = corona_history.read_excel(excel, landkreise, False, 8)
        colors_ax1, colors_ax2 = corona_history.get_colors(df1, df2)

        # assert keys have the correct values
        self.assertEqual(set(df1.drop(DEUTSCHLAND).index), set(colors_ax1.keys()))
        self.assertEqual(set(df2.drop(DEUTSCHLAND).index), set(colors_ax2.keys()))

        # assert values are valid farbcodes
        for colors_ax in (colors_ax1, colors_ax2):
            for color in colors_ax.values():
                self.assertRegex(color, r"^#[\da-fA-F]{6}$")


if __name__ == "__main__":
    unittest.main()
