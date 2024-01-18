from lldb import SBValue
from .abstractsynth import AbstractSynth


def qsharedpointer_summary(valobj: SBValue) -> str:
    addr = valobj.GetChildAtIndex(0).GetValueAsUnsigned()
    return hex(addr)


class QSharedPointerSynth(AbstractSynth):
    PROP_POINTER = 'pointer'
    PROP_VALUE = 'value'
    PROP_STRONG_REF = 'strongref'
    PROP_WEAK_REF = 'weakref'

    def get_child_index(self, name: str) -> int:
        if name == QSharedPointerSynth.PROP_POINTER:
            return 0
        elif self.num_children() > 1:
            if name == QSharedPointerSynth.PROP_VALUE:
                return 1
            elif name == QSharedPointerSynth.PROP_STRONG_REF:
                return 2
            elif name == QSharedPointerSynth.PROP_WEAK_REF:
                return 3
        return -1

    def update(self):
        p_value = self._valobj.GetChildMemberWithName('value')
        self._values = [self._valobj.CreateValueFromData(QSharedPointerSynth.PROP_POINTER, p_value.data, p_value.type)]

        if p_value.GetValueAsUnsigned():
            value = p_value.Dereference()
            d = self._valobj.GetChildMemberWithName('d').Dereference()
            self._values = [
                self._valobj.CreateValueFromData(self.PROP_POINTER, p_value.data, p_value.type),
                self._valobj.CreateValueFromData(self.PROP_VALUE, value.data, value.type),
                d.GetChildMemberWithName(self.PROP_STRONG_REF),
                d.GetChildMemberWithName(self.PROP_WEAK_REF)
            ]
        return False
