from typing import Iterable, Tuple

from gdb import Value
from .baseprinter import StructureOnlyPrinter

class QSharedPointerPrinter(StructureOnlyPrinter):
    PROP_VALUE = 'value'
    PROP_ADDRESS = 'address'
    PROP_WEAKREF = 'weakref'
    PROP_STRONGREF = 'strongref'

    def children(self) -> Iterable[Tuple[str, Value]]:
        value = self._valobj['value']
        if not value:
            yield QSharedPointerPrinter.PROP_VALUE, value
        else:
            yield QSharedPointerPrinter.PROP_VALUE, value.dereference()
            yield QSharedPointerPrinter.PROP_ADDRESS, value
            d = self._valobj['d']
            yield QSharedPointerPrinter.PROP_WEAKREF, d['weakref']
            yield QSharedPointerPrinter.PROP_STRONGREF, d['strongref']