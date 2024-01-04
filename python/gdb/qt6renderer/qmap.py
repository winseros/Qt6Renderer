from typing import Iterable, Tuple

from gdb import Value

from .baseprinter import StructureOnlyPrinter


class QMapPrinter(StructureOnlyPrinter):
    PROP_SIZE = 'size'
    PROP_DATA = 'data'

    def children(self) -> Iterable[Tuple[str, Value]]:
        d_d = self._valobj['d']['d']
        if not d_d:
            yield QMapPrinter.PROP_SIZE, 0
        else:
            m = d_d['m']
            yield QMapPrinter.PROP_DATA, m
