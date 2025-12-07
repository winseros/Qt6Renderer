from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qstring_summary_no_quotes(valobj: SBValue) -> str:
    sb_size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE)
    if not sb_size:
        return ''

    size = sb_size.GetValueAsSigned()
    if size <= 0:
        return ''

    sb_raw = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_RAW_DATA)
    if not sb_raw.IsValid():
        return ''

    # QString is char16_t in the C++ code.
    # But Python goes wild when string bytes have higher order values, like 65533,
    # because sint16 of such values get interpreted as negative numbers and Python
    # is unable to convert them to chars.

    data = sb_raw.GetPointeeData(0, size).uint16s

    result = ''
    for code in data:
        result += chr(code)
    return result


def qstring_summary(valobj: SBValue) -> str:
    text = qstring_summary_no_quotes(valobj)
    return text if len(text) else '""'


class QStringSynth(QArrayDataPointerSynth):
    pass
