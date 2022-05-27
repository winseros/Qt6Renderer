from lldb import SBValue, eBasicTypeUnsignedLongLong


def pointer_summary(valobj: SBValue):
    addr = valobj.GetChildAtIndex(0).GetValueAsUnsigned()
    return hex(addr)


class PointerSynth:
    _PROP_ADDRESS = '[address]'
    _PROP_DATA = '[data]'

    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._values = []
        process = valobj.GetProcess()
        self._is_null = False
        self._byte_order = process.GetByteOrder()
        self._byte_size = process.GetAddressByteSize()
        self._addr_type = valobj.GetTarget().GetBasicType(eBasicTypeUnsignedLongLong)

    def has_children(self) -> bool:
        return not self._is_null

    def num_children(self) -> int:
        return len(self._values)

    def get_child_index(self, name: str) -> int:
        if name == PointerSynth._PROP_ADDRESS:
            return 0
        if name == PointerSynth._PROP_DATA or name == '$$dereference$$':
            return 1
        else:
            return -1

    def get_child_at_index(self, index: int) -> SBValue:
        return self._valobj if self._is_null else self._values[index]

    def get_value(self):
        return self._valobj

    def update(self):
        self._is_null = self._valobj.GetValueAsUnsigned() == 0
        if not self._is_null:
            p_data = self._valobj.Dereference()
            self._values = [
                self._valobj.CreateValueFromData(PointerSynth._PROP_ADDRESS, self._valobj.GetData(), self._addr_type),
                self._valobj.CreateValueFromData(PointerSynth._PROP_DATA, p_data.GetData(), p_data.GetType())
            ]

        return False
