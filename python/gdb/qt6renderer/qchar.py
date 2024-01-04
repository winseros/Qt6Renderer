from .baseprinter import StringOnlyPrinter


class QCharPrinter(StringOnlyPrinter):
    def to_string(self) -> str:
        ucs = self._valobj['ucs']
        return ucs
