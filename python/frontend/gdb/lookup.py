from backend.gdb.native_types import Value
from frontend.gdb.qbytearrayprinter import QByteArrayPrinter
from frontend.gdb.qstringprinter import QStringPrinter


def print(valobj: Value):
    type_tag = valobj.type.tag
    if not type_tag:
        return None

    if type_tag.endswith('QByteArray'):
        return QByteArrayPrinter(valobj)
    elif type_tag.endswith('QString'):
        return QStringPrinter(valobj)

    return None
