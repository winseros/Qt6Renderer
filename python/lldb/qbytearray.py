from lldb import SBValue
from qarraydatapointer import QArrayDataPointerSynth


def qbytearray_summary(valobj):
    # type: (SBValue) -> str
    """Formats the QT QList type"""
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsUnsigned()
    return '[size]={}'.format(size)


class QByteArraySynth(QArrayDataPointerSynth):
    pass
