from .baseprinter import StringOnlyPrinter


class QStringPrinter(StringOnlyPrinter):
    def to_string(self) -> str:
        d = self._valobj['d']
        d_size = d['size']
        d_ptr = d['ptr']

        data = d_ptr.string('', 'replace', d_size)
        return data
