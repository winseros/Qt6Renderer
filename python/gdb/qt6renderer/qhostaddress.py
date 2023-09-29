from .baseprinter import StringOnlyPrinter
from gdb import Value


class QHostAddressPrinter(StringOnlyPrinter):
    def to_string(self) -> str:
        d = self._valobj['d']['d'].dereference()
        protocol = d['protocol']

        text = '(Invalid)'
        if protocol == 0:
            text = _format_as_v4(d)
        elif protocol == 1:
            text = _format_as_v6(d)
        return text


def _format_as_v4(addr: Value) -> str:
    a4 = int(addr['a'])

    a4, n4 = divmod(a4, 256)
    a4, n3 = divmod(a4, 256)
    a4, n2 = divmod(a4, 256)
    a4, n1 = divmod(a4, 256)

    return f'{n1}.{n2}.{n3}.{n4}'


def _format_as_v6(valobj: Value) -> str:
    a6 = valobj['a6']['c']

    text = ''
    for i in range(0, a6.type.sizeof, 2):
        if i > 0:
            text += ':'
        text += f'{int(a6[i]):02x}{int(a6[i + 1]):02x}'
    return text
