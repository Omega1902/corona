from datetime import datetime
import unittest
from landkreise import Landkreise
import corona_history


class TestLandkreise(unittest.TestCase):
    inzidenzen_result = [
        {
            "name": "SK Köln",
            datetime(2021, 6, 10, 0, 0): 20.2231347146,
            datetime(2021, 6, 9, 0, 0): 18.2927445827,
            datetime(2021, 6, 8, 0, 0): 23.7162216198,
            datetime(2021, 6, 7, 0, 0): 26.6577684874,
            datetime(2021, 6, 6, 0, 0): 27.5770018835,
            datetime(2021, 6, 5, 0, 0): 31.0700887888,
            datetime(2021, 6, 4, 0, 0): 32.8166322414,
        },
        {
            "name": "LK Nordfriesland",
            datetime(2021, 6, 10, 0, 0): 6.6284626185,
            datetime(2021, 6, 9, 0, 0): 10.2439876831,
            datetime(2021, 6, 8, 0, 0): 16.2698627908,
            datetime(2021, 6, 7, 0, 0): 21.090562877,
            datetime(2021, 6, 6, 0, 0): 22.8983254093,
            datetime(2021, 6, 5, 0, 0): 24.1035004309,
            datetime(2021, 6, 4, 0, 0): 27.7190254955,
        },
        {
            "name": "LK Oberbergischer Kreis",
            datetime(2021, 6, 10, 0, 0): 19.4812116579,
            datetime(2021, 6, 9, 0, 0): 26.4650422522,
            datetime(2021, 6, 8, 0, 0): 30.8758826275,
            datetime(2021, 6, 7, 0, 0): 31.6110226901,
            datetime(2021, 6, 6, 0, 0): 36.0218630655,
            datetime(2021, 6, 5, 0, 0): 39.329993347,
            datetime(2021, 6, 4, 0, 0): 43.0056936598,
        },
        {
            "name": "SK Wolfsburg",
            datetime(2021, 6, 10, 0, 0): 7.2364136334,
            datetime(2021, 6, 9, 0, 0): 14.4728272668,
            datetime(2021, 6, 8, 0, 0): 25.7294706965,
            datetime(2021, 6, 7, 0, 0): 32.1618383707,
            datetime(2021, 6, 6, 0, 0): 30.5537464521,
            datetime(2021, 6, 5, 0, 0): 28.9456545336,
            datetime(2021, 6, 4, 0, 0): 35.3780222077,
        },
    ]
    dates = [
        datetime(2021, 6, 4, 0, 0),
        datetime(2021, 6, 5, 0, 0),
        datetime(2021, 6, 6, 0, 0),
        datetime(2021, 6, 7, 0, 0),
        datetime(2021, 6, 8, 0, 0),
        datetime(2021, 6, 9, 0, 0),
        datetime(2021, 6, 10, 0, 0),
    ]
    germany_result = {
        datetime(2021, 6, 10, 0, 0): 29.677739690824133,
        datetime(2021, 6, 9, 0, 0): 26.2532926184853,
        datetime(2021, 6, 8, 0, 0): 24.71541768677133,
        datetime(2021, 6, 7, 0, 0): 24.289766611066298,
        datetime(2021, 6, 6, 0, 0): 22.920228262964493,
        datetime(2021, 6, 5, 0, 0): 20.764317588560164,
        datetime(2021, 6, 4, 0, 0): 19.255300356893997,
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

    def test_convert_to_printable_list(self):
        header, table = corona_history.convert_to_printable_list(self.dates, self.inzidenzen_result)
        self.assertEqual(self.header, header)
        self.assertEqual(self.table, table)

    def test_convert_to_graph_data(self):
        x_axis_labels, kreis, graph_data = corona_history.convert_to_graph_data(self.dates, self.inzidenzen_result)
        self.assertEqual(self.x_axis_labels, x_axis_labels)
        self.assertEqual(self.kreis, kreis)
        self.assertEqual(self.graph_data, graph_data)

    def test_set_graph_title(self):
        title = corona_history.set_graph_title(self.dates)
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

    def test_get_lines(self):
        tests = (
            ((None, None), []),
            (([], None), []),
            (([[], None], None), []),
            (([[], []], None), []),
            (([[1, 2, 3], [3, 4, 2], [2, 4, 0]], None), []),
            (([[1, 2, 3], [3, 4, 5], [5, 6, 0]], None), [10]),
            (([[1, 2, 3], [29.999, 4, 5], [5, 6, 7]], None), [10]),
            (([[1, 2, 3], [30.001, 4, 5], [5, 6, 7]], None), [10, 35]),
            (([[1, 2, 3], [30.001, 46, 5], [5, 6, 7]], None), [10, 35, 50]),
            (([[1, 2, 3], [30.001, 46, 5], [85, 6, 7]], None), [10, 35, 50, 100]),
            (([[1, 2, 3], [30.001, 46, 5], [130, 6, 7]], None), [10, 35, 50, 100]),
            (([[1, 2, 3], [30.001, 46, 5], [190, 6, 7]], None), [10, 35, 50, 100, 150, 200]),
            (([[1, 2, 3], [30.001, 46, 5], [190, 6, 7]], []), [10, 35, 50, 100, 150, 200]),
            (([[1, 2, 3], [30.001, 46, 5], [190, 6, 7]], [0]), [10, 35, 50, 100, 150, 200]),
            (([[1, 2, 3], [30.001, 46, 5], [190, 6, 7]], [100, 200, 0]), [10, 35, 50, 100, 150, 200]),
            (([[1, 2, 3], [30.001, 46, 5], [190, 6, 7]], [100, 200, 300]), [10, 35, 50, 100, 150, 200, 250, 300]),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(corona_history.get_lines(*test[0]), test[1])


if __name__ == "__main__":
    unittest.main()
