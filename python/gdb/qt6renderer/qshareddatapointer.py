from typing import Iterable, Tuple

from gdb import Value
from .baseprinter import StructureOnlyPrinter


class QSharedDataPointerPrinter(StructureOnlyPrinter):
    PROP_POINTER = 'pointer'
    PROP_VALUE = 'value'

    def children(self) -> Iterable[Tuple[str, Value]]:
        d = self._valobj['d']
        if not d:
            yield QSharedDataPointerPrinter.PROP_POINTER, d
        else:
            if d.type != d.dynamic_type:
                d = d.dynamic_cast(d.dynamic_type)
            yield QSharedDataPointerPrinter.PROP_VALUE, d.dereference()
            yield QSharedDataPointerPrinter.PROP_POINTER, d
