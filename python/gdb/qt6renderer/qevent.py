from typing import Iterable, Tuple

from gdb import Value, lookup_type
from .baseprinter import StructureOnlyPrinter


class QEventPrinter(StructureOnlyPrinter):
    PROP_TYPE = 'type'

    def children(self) -> Iterable[Tuple[str, Value]]:
        event_type = lookup_type('QEvent::Type')

        yield QEventPrinter.PROP_TYPE, self._valobj['t'].cast(event_type)

        for field in self._valobj.type.fields():
            if field.name.startswith('m_'):
                yield field.name, self._valobj[field.name]
