from lldb import SBValue, SBData, SBType, eBasicTypeUnsignedLongLong


def qsharedpointer_summary(valobj: SBValue):
    addr = valobj.GetChildAtIndex(0).GetValueAsUnsigned()
    return hex(addr)


class QSharedPointerSynth:
    _PROP_ADDRESS = '[address]'
    _PROP_DATA = '[data]'
    _PROP_STRONG_REF = '[strong_ref]'
    _PROP_WEAK_REF = '[weak_ref]'

    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._values = []
        process = valobj.GetProcess()
        self._byte_order = process.GetByteOrder()
        self._byte_size = process.GetAddressByteSize()
        self._addr_type = valobj.GetTarget().GetBasicType(eBasicTypeUnsignedLongLong)

    def has_children(self) -> bool:
        return True

    def num_children(self) -> int:
        return len(self._values)

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

    def get_child_at_index(self, index: int) -> SBValue:
        return self._values[index]

    def get_value(self):
        return self._valobj

    def update(self):
        value = self._valobj.GetChildMemberWithName('value')
        d = self._valobj.GetChildMemberWithName('d').Dereference()
        strong_ref = d.GetChildMemberWithName('strongref')
        weak_ref = d.GetChildMemberWithName('weakref')
        data = value.Dereference()
        self._values = [
            self._valobj.CreateValueFromData(QSharedPointerSynth._PROP_ADDRESS, value.GetData(), self._addr_type),
            self._valobj.CreateValueFromData(QSharedPointerSynth._PROP_DATA, data.GetData(), data.GetType()),
            self._valobj.CreateValueFromData(QSharedPointerSynth._PROP_STRONG_REF, strong_ref.GetData(), strong_ref.GetType()),
            self._valobj.CreateValueFromData(QSharedPointerSynth._PROP_WEAK_REF, weak_ref.GetData(), weak_ref.GetType()),
        ]

        return False
