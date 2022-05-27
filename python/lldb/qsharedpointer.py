from lldb import SBValue, eBasicTypeUnsignedLongLong
from abstractsynth import AbstractSynth

def qsharedpointer_summary(valobj: SBValue):
    addr = valobj.GetChildAtIndex(0).GetValueAsUnsigned()
    return hex(addr)


class QSharedPointerSynth(AbstractSynth):
    _PROP_ADDRESS = 'address'
    _PROP_DATA = 'data'
    _PROP_STRONG_REF = 'strongref'
    _PROP_WEAK_REF = 'weakref'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._addr_type = valobj.GetTarget().GetBasicType(eBasicTypeUnsignedLongLong)

    def get_child_index(self, name: str) -> int:
        if name == QSharedPointerSynth._PROP_ADDRESS:
            return 0
        elif name == QSharedPointerSynth._PROP_DATA or name == '$$dereference$$':
            return 1
        elif name == QSharedPointerSynth._PROP_STRONG_REF:
            return 2
        elif name == QSharedPointerSynth._PROP_WEAK_REF:
            return 3
        else:
            return -1

    def update(self):
        value = self._valobj.GetChildMemberWithName('value')
        d = self._valobj.GetChildMemberWithName('d').Dereference()
        data = value.Dereference()
        self._values = [
            self._valobj.CreateValueFromData(self._PROP_ADDRESS, value.GetData(), self._addr_type),
            self._valobj.CreateValueFromData(self._PROP_DATA, data.GetData(), data.GetType()),
            d.GetChildMemberWithName(self._PROP_STRONG_REF),
            d.GetChildMemberWithName(self._PROP_WEAK_REF)
        ]
        return False
