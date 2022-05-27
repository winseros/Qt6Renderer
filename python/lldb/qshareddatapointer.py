from lldb import SBValue, eBasicTypeUnsignedLongLong
from abstractsynth import AbstractSynth


def qshareddatapointer_summary(valobj: SBValue):
    addr = valobj.GetChildAtIndex(0).GetValueAsUnsigned()
    return hex(addr)


class QSharedDataPointerSynth(AbstractSynth):
    _PROP_ADDRESS = '[address]'
    _PROP_DATA = '[data]'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        process = valobj.GetProcess()
        self._byte_order = process.GetByteOrder()
        self._byte_size = process.GetAddressByteSize()
        self._addr_type = valobj.GetTarget().GetBasicType(eBasicTypeUnsignedLongLong)

    def get_child_index(self, name: str) -> int:
        if name == QSharedDataPointerSynth._PROP_ADDRESS:
            return 0
        if name == QSharedDataPointerSynth._PROP_DATA or name == '$$dereference$$':
            return 1
        else:
            return -1

    def update(self):
        pointer = self._valobj.GetChildMemberWithName('d')
        is_null = pointer.GetValueAsUnsigned() == 0
        if not is_null:
            data = pointer.Dereference()
            print(data)
            self._values = [
                self._valobj.CreateValueFromData(QSharedDataPointerSynth._PROP_ADDRESS, pointer.GetData(), self._addr_type),
                self._valobj.CreateValueFromData(QSharedDataPointerSynth._PROP_DATA, data.GetData(), data.GetType())
            ]

        return False
