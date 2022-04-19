import unittest

from corona import Connector


class TestCorona(unittest.IsolatedAsyncioTestCase):
    async def test_corona_germany(self):
        async with Connector() as con:
            result = await con.get_germany()
            self.assertIsInstance(result, (float, int))
            # assert result == 14.5 # enable line and put the real result of the current day for testing


if __name__ == "__main__":
    unittest.main()
