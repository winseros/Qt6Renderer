from typing import Iterable, Tuple

from gdb import Value
from .baseprinter import StringAndStructurePrinter
from .helpers import DateTimeHelpers


class QTimePrinter(StringAndStructurePrinter):

    def to_string(self) -> str:
        children = list(self.children())
        if len(children) < 2:
            return DateTimeHelpers.VAL_INVALID

        hour = children[0][1]
        minute = children[1][1]
        second = children[2][1]
        msecond = children[3][1]

        return f'{hour:02d}:{minute:02d}:{second:02d}.{msecond:03d}'

    def children(self) -> Iterable[Tuple[str, Value]]:
        mds = self._valobj['mds']

        if mds == -1:
            yield DateTimeHelpers.PROP_INVALID, True
            return

        (hours, minutes, seconds, milliseconds) = DateTimeHelpers.parse_time(int(mds))

        yield DateTimeHelpers.PROP_HOURS, hours
        yield DateTimeHelpers.PROP_MINUTES, minutes
        yield DateTimeHelpers.PROP_SECONDS, seconds
        yield DateTimeHelpers.PROP_MILLISECONDS, milliseconds
