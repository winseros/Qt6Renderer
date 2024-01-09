from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qstring_summary(valobj: SBValue):
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsSigned()
    if not size:
        return '""'

    data = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_RAW_DATA).GetPointeeData(0, size).sint16s

    result = ''
    for code in data:
        result += chr(code)
    return result


class QStringSynth(QArrayDataPointerSynth):
    pass
