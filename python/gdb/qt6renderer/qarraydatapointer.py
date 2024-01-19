from .baseprinter import StringAndStructurePrinter


class QArrayDataPointerPrinter(StringAndStructurePrinter):
    PROP_SIZE = 'size'
    PROP_CAPACITY = 'capacity'
    PROP_RAW_DATA = 'raw_data'

    def children(self):
        d = self._valobj['d']
        d_size = d['size']

        yield QArrayDataPointerPrinter.PROP_SIZE, d_size

        if d_size <= 0:
            return

        d_d_alloc = d['d']['alloc']

        if d_d_alloc == 0 or d_size > d_d_alloc:
            # half-initialized structure
            return

        yield QArrayDataPointerPrinter.PROP_CAPACITY, d_d_alloc
        yield QArrayDataPointerPrinter.PROP_RAW_DATA, d

        d_ptr = d['ptr']
        for i in range(d_size):
            chr_ptr = d_ptr + i
            yield f'[{i}]', chr_ptr.dereference()

    def to_string(self) -> str:
        d = self._valobj['d']
        d_size = d['size']
        return f'size={d_size}'
