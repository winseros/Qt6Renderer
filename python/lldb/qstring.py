from lldb import SBValue
from qarraydatapointer import QArrayDataPointerSynth


def qstring_unquoted(valobj: SBValue):
    length = valobj.GetNumChildren()
    if not length:
        return '""'

    chars = [valobj.GetChildAtIndex(i).GetValueAsUnsigned() for i in
             range(QArrayDataPointerSynth.RANGE_START_OFFSET, length)]
    text = ''.join(chr(char) for char in chars)
    return text


def qstring_summary(valobj):
    text = qstring_unquoted(valobj)
    return '"' + text + '"'


class QStringSynth(QArrayDataPointerSynth):
    pass
