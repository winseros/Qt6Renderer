from lldb import SBValue
from qstring import qstring_summary
from abstractsynth import AbstractSynth


def qtimezone_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        id = valobj.GetChildMemberWithName(QTimeZoneSynth.PROP_ID)
        id_text = qstring_summary(id)
        return id_text
    else:
        return '(Null)'


class QTimeZoneSynth(AbstractSynth):
    PROP_ID = "[id]"

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._byte_array_type = valobj.GetFrame().GetModule().FindFirstType('QByteArray')

    def get_child_index(self, name: str) -> int:
        if name == QTimeZoneSynth.PROP_ID:
            return 0
        else:
            return -1

    def update(self):
        ptr = self._valobj.GetChildMemberWithName('d').GetChildMemberWithName('d').GetValueAsUnsigned()
        if ptr:
            id = self._valobj.CreateValueFromAddress(QTimeZoneSynth.PROP_ID, ptr + 16, self._byte_array_type)
            self._values = [id]

        return False
