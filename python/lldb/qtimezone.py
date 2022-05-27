from lldb import SBValue
from qstring import qstring_summary


def qtimezone_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        id = valobj.GetChildMemberWithName(QTimeZoneSynth.PROP_ID)
        id_text = qstring_summary(id)
        return id_text
    else:
        return '(Null)'


class QTimeZoneSynth:
    PROP_ID = "[id]"

    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._values = []
        self._byte_array_type = valobj.GetFrame().GetModule().FindFirstType('QByteArray')

    def has_children(self) -> bool:
        return len(self._values) > 0

    def num_children(self) -> int:
        return len(self._values)

    def get_child_index(self, name: str) -> int:
        if name == QTimeZoneSynth.PROP_ID:
            return 0
        else:
            return -1

    def get_child_at_index(self, index: int) -> SBValue:
        return self._values[index]

    def get_value(self):
        return self._valobj

    def update(self):
        ptr = self._valobj.GetChildMemberWithName('d').GetChildMemberWithName('d').GetValueAsUnsigned()
        if ptr:
            id = self._valobj.CreateValueFromAddress(QTimeZoneSynth.PROP_ID, ptr + 16, self._byte_array_type)
            self._values = [id]

        return False
