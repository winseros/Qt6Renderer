from abstractsynth import AbstractSynth
from lldb import SBValue, eBasicTypeUnsignedShort


class QEventSynth(AbstractSynth):
    PROP_TYPE = 'type'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._type_event = valobj.GetFrame().GetModule().FindFirstType('QEvent::Type')
        self._type_ushort = valobj.GetTarget().GetBasicType(eBasicTypeUnsignedShort)

    def get_child_index(self, name: str) -> int:
        if name == self.PROP_TYPE:
            return 0
        else:
            return -1

    def update(self) -> bool:
        addr = self._valobj.load_addr
        type_short = self._valobj.CreateValueFromAddress(self.PROP_TYPE, addr + 8, self._type_ushort)

        if self._type_event.IsValid():
            type_evt = type_short.Cast(self._type_event)
            self._values = [type_evt]
        else:
            self._values = [type_short]

        self._values.extend(self._valobj.children)

        return False
