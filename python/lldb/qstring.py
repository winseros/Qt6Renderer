from lldb import SBValue
from qarraydatapointer import QArrayDataPointerSynth


def qstring_summary(valobj):
    # type: (SBValue) -> str
    """Formats the QT QString type"""
    length = valobj.GetNumChildren()
    if not length:
        return '""'

    chars = [valobj.GetChildAtIndex(i).GetValueAsUnsigned() for i in
             range(QArrayDataPointerSynth.RANGE_START_OFFSET, length)]
    text = ''.join(chr(char) for char in chars)
    return '"' + text + '"'


class QStringSynth(QArrayDataPointerSynth):
    pass
