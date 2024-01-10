from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qlist_summary(valobj: SBValue) -> str:
    size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE).GetValueAsUnsigned()
    return f'size={size}'


class QListSynth(QArrayDataPointerSynth):
    pass
