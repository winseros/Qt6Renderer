from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qbytearray_summary(valobj: SBValue):
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsSigned()
    return f'size={size}'


class QByteArraySynth(QArrayDataPointerSynth):
    pass