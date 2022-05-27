from lldb import SBValue


class QMapSynth:
    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._map = None

    def num_children(self) -> int:
        return False if self._map is None else self._map.GetNumChildren()

    def get_child_index(self, name: str) -> int:
        return -1 if self._map is None else self._map.GetIndexOfChildWithName(name)

    def get_child_at_index(self, index: int) -> SBValue:
        return None if self._map is None else self._map.GetChildAtIndex(index)

    def get_value(self):
        return self._valobj

    def update(self):
        d_d = self._valobj.GetChildMemberWithName('d') \
            .GetChildMemberWithName('d')

        self._map = None if not d_d.GetValueAsUnsigned() else d_d.GetChildMemberWithName('m')
        return False
