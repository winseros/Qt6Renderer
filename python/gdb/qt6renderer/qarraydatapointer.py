from .baseprinter import StringAndStructurePrinter


class QArrayDataPointerPrinter(StringAndStructurePrinter):
    PROP_SIZE = 'size'
    PROP_CAPACITY = 'capacity'
    PROP_RAW_DATA = 'raw_data'

    def children(self):
        d = self._valobj['d']
        d_size = d['size']
        d_ptr = d['ptr']
        d_d_alloc = d['d']['alloc']

        yield QArrayDataPointerPrinter.PROP_SIZE, d_size
        yield QArrayDataPointerPrinter.PROP_CAPACITY, d_d_alloc
        yield QArrayDataPointerPrinter.PROP_RAW_DATA, d

        for i in range(d_size):
            chr_ptr = d_ptr + i
            yield f'[{i}]', chr_ptr.dereference()

    def to_string(self) -> str:
        d = self._valobj['d']
        d_size = d['size']
        return f'size={d_size}'
