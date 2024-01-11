from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qbytearray_summary(valobj: SBValue):
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsSigned()
    return f'size={size}'

def qbytearray_string_summary(valobj: SBValue):
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsSigned()
    if not size:
        return '""'

    data = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_RAW_DATA).GetPointeeData(0, size).sint8s

    result = ''
    for code in data:
        result += chr(code)
    return result

class QByteArraySynth(QArrayDataPointerSynth):
    pass