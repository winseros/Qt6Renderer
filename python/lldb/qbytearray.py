from lldb import SBValue
from qarraydatapointer import QArrayDataPointerSynth


def qbytearray_summary(valobj):
    # type: (SBValue) -> str
    """Formats the QT QList type"""
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsUnsigned()
    return f'size={size}'


class QByteArraySynth(QArrayDataPointerSynth):
    pass
