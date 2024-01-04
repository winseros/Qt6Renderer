from typing import Iterable, Tuple

from gdb import Value

from .baseprinter import StructureOnlyPrinter


class QScopedPointerPrinter(StructureOnlyPrinter):
    PROP_VALUE = 'value'
    PROP_POINTER = 'pointer'

    def children(self) -> Iterable[Tuple[str, Value]]:
        d = self._valobj['d']
        if not d:
            yield QScopedPointerPrinter.PROP_VALUE, d
        else:
            yield QScopedPointerPrinter.PROP_VALUE, d.dereference()
            yield QScopedPointerPrinter.PROP_POINTER, d
