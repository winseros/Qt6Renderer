from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qbytearray_summary(valobj: SBValue):
    sb_size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE)
    if not sb_size:
        return 'size=0'

    size = sb_size.GetValueAsSigned()
    return f'size={size}'


def qbytearray_string_summary(valobj: SBValue):
    sb_size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE)
    if not sb_size:
        return '""'

    size = sb_size.GetValueAsSigned()
    if size <= 0:
        return '""'

    sb_raw = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_RAW_DATA)
    if not sb_raw:
        return '""'

    data = sb_raw.GetPointeeData(0, size).sint8s

    result = ''
    for code in data:
        result += chr(code)
    return result


class QByteArraySynth(QArrayDataPointerSynth):
    pass
