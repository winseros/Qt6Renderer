from typing import Iterable, Tuple

from gdb import Value
from .baseprinter import StructureOnlyPrinter


class QSharedDataPointerPrinter(StructureOnlyPrinter):
    PROP_RAW_POINTER = 'raw_pointer'
    PROP_DATA = 'data'

    def children(self) -> Iterable[Tuple[str, Value]]:
        d = self._valobj['d']
        yield QSharedDataPointerPrinter.PROP_RAW_POINTER, d

        if d:
            if d.type != d.dynamic_type:
                d = d.dynamic_cast(d.dynamic_type)
            yield QSharedDataPointerPrinter.PROP_DATA, d.dereference()
