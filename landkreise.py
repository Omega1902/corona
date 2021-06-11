from enum import Enum
from typing import Iterable, Optional, List

class Landkreise(Enum):
    AURICH               = ( 51, "LK Aurich")
    BERLIN_MITTE         = (413, "SK Berlin Mitte")
    HAMBURG              = ( 16, "SK Hamburg")
    HANNOVER             = ( 27, "Region Hannover", "Hannover")
    KOELN                = ( 80, "SK Köln")
    LUEBECK              = (  3, "SK Lübeck")
    NORDFRIESLAND        = (  7, "LK Nordfriesland")
    OBERBERGISCHER_KREIS = ( 87, "LK Oberbergischer Kreis")
    OSTHOLSTEIN          = (  8, "LK Ostholstein")
    WOLFSBURG            = ( 19, "SK Wolfsburg")

    def __init__(self, lk_id: int, lk_name: str, name: Optional[str] = None):
        """Inits a Landkreis.

        Args:
            id (int): ID used by the rki dashboard. Needs to be unique.
            lk_name (str): Landkreis name used by the rki dashboard. Needs to be unique.
            name (Optional[str]): String to display for user. Default will use lk_name and remove prefix 'LK ' and 'SK '
        """
        self._lk_name = lk_name
        if name is None:
            if lk_name.startswith("LK ") or lk_name.startswith("SK "):
                self._name = lk_name[3:]
            else:
                self._name = lk_name
        else:
            self._name = name
        self._value_ = lk_id

    @property
    def name(self):
        return self._name

    @property
    def lk_name(self):
        return self._lk_name

    @property
    def id(self):
        return self._value_

    @staticmethod
    def find_by_id(lk_id) -> Optional["Landkreise"]:
        result = [lk for lk in Landkreise if lk.id == lk_id]
        return None if len(result) != 1 else result[0]

    @classmethod
    def find_by_ids(cls, lk_ids: Iterable[int]) -> List["Landkreise"]:
        """Will return a list of all Landkreise of the given ids.
        If an id does not exist, the None paramter returned by find_by_id will not be contained in this list.
        If lk_ids is None or does not contain a valid lk_id, the result will be an empty list.

        Args:
            lk_ids (Iterable[int]): lk_ids to convert to Landkreise

        Returns:
            list[Landkreise]: List of Landkreise
        """
        result = []
        for lk_id in lk_ids:
            landkreis = cls.find_by_id(lk_id)
            if landkreis is not None:
                result.append(landkreis)
        return result

    @staticmethod
    def find_by_lk_name(lk_name) -> Optional["Landkreise"]:
        result = [lk for lk in Landkreise if lk.lk_name == lk_name]
        return None if len(result) != 1 else result[0]

    @classmethod
    def find_by_lk_names(cls, lk_names: Iterable[str]) -> List["Landkreise"]:
        """Will return a list of all Landkreise of the given lk_names.
        If an lk_name does not exist, the None paramter returned by find_by_lk_name will not be contained in this list.
        If lk_names is None or does not contain a valid lk_name, the result will be an empty list.

        Args:
            lk_names (Iterable[str]): lk_names to convert to Landkreise

        Returns:
            list[Landkreise]: List of Landkreise
        """
        result = []
        for lk_name in lk_names:
            landkreis = cls.find_by_lk_name(lk_name)
            if landkreis is not None:
                result.append(landkreis)
        return result

    def __str__(self):
        return self.name
