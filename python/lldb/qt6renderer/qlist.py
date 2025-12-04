from lldb import SBValue
from .qarraydatapointer import QArrayDataPointerSynth


def qlist_summary(valobj: SBValue) -> str:
    sb_size = valobj.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE)
    if not sb_size:
        return 'size=0'

    size = sb_size.GetValueAsUnsigned()
    return f'size={size}'


class QListSynth(QArrayDataPointerSynth):
    pass
