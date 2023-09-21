from gdb import Value, lookup_type


class QStringPrinter:
    def __init__(self, valobj: Value):
        self._valobj = valobj

    def children(self):
        d = self._valobj['d']
        d_size = d['size']

        d_ptr = d['ptr']

        d_d = d['d']
        d_d_alloc = d_d['alloc']

        for i in range(0, 4):
            if i == 0:
                data = d_ptr.string('', 'replace', d_size)
                yield ('data', data)
            elif i == 1:
                yield ('size', d_size)
            elif i == 2:
                yield ('capacity', d_d_alloc)
            elif i == 3:
                yield ('raw_data', d)

    def to_string(self) -> str:
        d = self._valobj['d']
        d_size = d['size']
        d_ptr = d['ptr']

        data = d_ptr.string('', 'replace', d_size)
        return data

    def display_hint(self):
        return 'string'
