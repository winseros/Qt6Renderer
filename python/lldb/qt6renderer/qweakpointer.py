from lldb import SBValue
from .abstractsynth import AbstractSynth


def qweakpointer_summary(valobj: SBValue) -> str:
    addr = valobj.GetChildAtIndex(0).GetValueAsUnsigned()
    return hex(addr)


class QWeakPointerSynth(AbstractSynth):
    PROP_POINTER = 'pointer'
    PROP_VALUE = 'value'
    PROP_D = 'd'

    def get_child_index(self, name: str) -> int:
        if name == QWeakPointerSynth.PROP_POINTER:
            return 0
        elif name == QWeakPointerSynth.PROP_VALUE and self.num_children() > 1:
            return 1
        elif name == QWeakPointerSynth.PROP_D and self.num_children() > 1:
            return 2
        return -1

    def update(self):
        pointer = self._valobj.GetChildMemberWithName('value')
        self._values = [self._valobj.CreateValueFromData(QWeakPointerSynth.PROP_POINTER, pointer.data, pointer.type)]

        if pointer.GetValueAsUnsigned():
            value = pointer.Dereference()
            self._values.append(self._valobj.CreateValueFromData(QWeakPointerSynth.PROP_VALUE, value.data, value.type))
            self._values.append(self._valobj.GetChildMemberWithName('d'))
        return False
