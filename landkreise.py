from enum import Enum
from typing import Optional

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


    def __init__(self, id: int, lk_name: str, name: Optional[str] = None):
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
        self._value_ = id

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
    def find_by_id(id) -> Optional["Landkreise"]:
        result = [lk for lk in Landkreise if lk.id == id]
        if len(result) == 1:
            return result[0]
        else:
            return None

    @staticmethod
    def find_by_lk_bez(lk_name) -> Optional["Landkreise"]:
        result = [lk for lk in Landkreise if lk.lk_name == lk_name]
        if len(result) == 1:
            return result[0]
        else:
            return None
    
    def __str__(self):
        return self.name
