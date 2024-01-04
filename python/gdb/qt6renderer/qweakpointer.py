from typing import Iterable, Tuple
from gdb import Value

from .baseprinter import StructureOnlyPrinter

class QWeakPointerPrinter(StructureOnlyPrinter):
    PROP_POINTER = 'pointer'
    PROP_VALUE = 'value'
    PROP_WEAKREF = 'weakref'
    PROP_STRONGREF = 'strongref'

    def children(self) -> Iterable[Tuple[str, Value]]:
        value = self._valobj['value']
        if not value:
            yield QWeakPointerPrinter.PROP_VALUE, value
        else:
            yield QWeakPointerPrinter.PROP_VALUE, value.dereference()
            yield QWeakPointerPrinter.PROP_POINTER, value
            d = self._valobj['d']
            yield QWeakPointerPrinter.PROP_WEAKREF, d['weakref']
            yield QWeakPointerPrinter.PROP_STRONGREF, d['strongref']
