from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qstring_summary(valobj: SBValue):
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsSigned()
    data = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_RAW_DATA).GetPointeeData(0, size).sint16s

    result = 'u"'
    for code in data:
        result += chr(code)
    result += '"'
    return result


class QStringSynth(QArrayDataPointerSynth):
    pass
