from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qstring_summary_no_quotes(valobj: SBValue) -> str:
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsSigned()
    if not size:
        return ''

    data = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_RAW_DATA).GetPointeeData(0, size).sint16s

    result = ''
    for code in data:
        result += chr(code)
    return result


def qstring_summary(valobj: SBValue) -> str:
    text = qstring_summary_no_quotes(valobj)
    return text if len(text) else '""'


class QStringSynth(QArrayDataPointerSynth):
    pass
