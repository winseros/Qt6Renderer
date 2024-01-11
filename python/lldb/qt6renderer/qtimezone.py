from lldb import SBValue
from .abstractsynth import AbstractSynth
from .qshareddata import QSharedData
from .qbytearray import qbytearray_string_summary


def qtimezone_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        id = valobj.GetChildMemberWithName(QTimeZonePrivate.PROP_ID)
        text = qbytearray_string_summary(id)
        return text
    else:
        return 'NULL'


class QTimeZoneSynth(AbstractSynth):
    def get_child_index(self, name: str) -> int:
        if name == QTimeZonePrivate.PROP_ID:
            return 0
        else:
            return -1

    def update(self):
        d = self._valobj.GetChildMemberWithName('d').GetChildMemberWithName('d')
        if d.GetValueAsUnsigned():
            priv = QTimeZonePrivate(d)
            self._values = [priv.id()]

        return False


class QTimeZonePrivate(QSharedData):
    PROP_ID = "id"

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_gap_field(8)
        self.add_named_type_field(QTimeZonePrivate.PROP_ID, 'QByteArray')

    def id(self) -> SBValue:
        pass
