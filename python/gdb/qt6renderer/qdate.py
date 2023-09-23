from typing import Iterable, Tuple

from gdb import Value
from .baseprinter import StringAndStructurePrinter
from .helpers import DateTimeHelpers


class QDatePrinter(StringAndStructurePrinter):
    def to_string(self) -> str:
        jd = self._valobj['jd']
        year, date, month = DateTimeHelpers.parse_julian_date(int(jd))
        return f'{year}-{date:02d}-{month:02d}' if year else DateTimeHelpers.VAL_INVALID

    def children(self) -> Iterable[Tuple[str, Value]]:
        jd = self._valobj['jd']
        year, month, day = DateTimeHelpers.parse_julian_date(int(jd))
        if year:
            yield DateTimeHelpers.PROP_YEAR, year
            yield DateTimeHelpers.PROP_MONTH, month
            yield DateTimeHelpers.PROP_DAY, day
        else:
            yield DateTimeHelpers.PROP_INVALID, True
