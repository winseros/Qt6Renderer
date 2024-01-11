from lldb import SBValue
from .abstractsynth import AbstractSynth


def qscopedpointer_summary(valobj: SBValue) -> str:
    addr = valobj.GetChildAtIndex(0).GetValueAsUnsigned()
    return hex(addr)


class QScopedPointerSynth(AbstractSynth):
    PROP_POINTER = 'pointer'
    PROP_VALUE = 'value'

    def get_child_index(self, name: str) -> int:
        if name == QScopedPointerSynth.PROP_POINTER:
            return 0
        elif name == QScopedPointerSynth.PROP_VALUE and self.num_children() > 1:
            return 1
        return -1

    def update(self):
        d = self._valobj.GetChildMemberWithName('d')
        self._values = [self._valobj.CreateValueFromData(QScopedPointerSynth.PROP_POINTER, d.data, d.type)]

        if d.GetValueAsUnsigned():
            value = d.Dereference()
            self._values = [
                self._valobj.CreateValueFromData(self.PROP_POINTER, d.data, d.type),
                self._valobj.CreateValueFromData(self.PROP_VALUE, value.data, value.type),
            ]
        return False
