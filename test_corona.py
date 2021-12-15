import unittest
import asyncio
from corona import Connector


async def check_germany():
    async with Connector() as con:
        result = await con.get_germany()
    assert isinstance(result, float)
    # assert result == 14.5 # enable line and put the real result of the current day for testing


class TestCorona(unittest.TestCase):
    def test_corona_germany(self):
        asyncio.run(check_germany())


if __name__ == "__main__":
    unittest.main()
