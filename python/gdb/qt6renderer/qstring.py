from .baseprinter import StringAndStructurePrinter


class QStringPrinter(StringAndStructurePrinter):
    PROP_SIZE = 'size'
    PROP_CAPACITY = 'capacity'
    PROP_RAW_DATA = 'raw_data'
    PROP_DATA = 'data'

    def children(self):
        d = self._valobj['d']
        d_size = d['size']
        d_ptr = d['ptr']
        d_d_alloc = d['d']['alloc']

        data = d_ptr.string('', 'replace', d_size)

        yield QStringPrinter.PROP_SIZE, d_size
        yield QStringPrinter.PROP_CAPACITY, d_d_alloc
        yield QStringPrinter.PROP_RAW_DATA, d
        yield QStringPrinter.PROP_DATA, data

    def to_string(self) -> str:
        d = self._valobj['d']
        d_size = d['size']
        d_ptr = d['ptr']

        data = d_ptr.string('', 'replace', d_size)
        return data
