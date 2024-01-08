from lldb import SBValue
from .abstractsynth import AbstractSynth


def qshareddatapointer_summary(valobj: SBValue):
    addr = valobj.GetChildAtIndex(0).GetValueAsUnsigned()
    return hex(addr)


class QSharedDataPointerSynth(AbstractSynth):
    PROP_POINTER = 'pointer'
    PROP_VALUE = 'value'

    def get_child_index(self, name: str) -> int:
        if name == QSharedDataPointerSynth.PROP_POINTER:
            return 0
        elif self.num_children() > 1 and name == QSharedDataPointerSynth.PROP_VALUE:
            return 1
        else:
            return -1

    def update(self) -> bool:
        d = self._valobj.GetChildMemberWithName('d')

        self._values.append(
            self._valobj.CreateValueFromData(QSharedDataPointerSynth.PROP_POINTER, d.data, d.type))

        if d.GetValueAsUnsigned():
            value = d.Dereference()
            if value.IsValid():
                self._values.append(
                    self._valobj.CreateValueFromData(QSharedDataPointerSynth.PROP_VALUE, value.data, value.type))

        return False
