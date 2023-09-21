from gdb import Value
from qbitarray import QBitArrayPrinter
from qstring import QStringPrinter


def pp_lookup(valobj: Value):
    type_tag = valobj.type.tag
    if not type_tag:
        return None

    if type_tag.endswith('QBitArray'):
        return QBitArrayPrinter(valobj)
    elif type_tag.endswith('QString'):
        return QStringPrinter(valobj)

    return None
