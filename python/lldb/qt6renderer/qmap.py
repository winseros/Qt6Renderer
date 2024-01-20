from .abstractsynth import AbstractSynth


class QMapSynth(AbstractSynth):
    def get_child_index(self, name: str) -> int:
        if name == 'm':
            return 0
        return -1

    def update(self):
        d_d = self._valobj.GetChildMemberWithName('d') \
            .GetChildMemberWithName('d')

        if d_d.GetValueAsUnsigned():
            map = d_d.GetChildMemberWithName('m')
            map_deref_type = map.type.GetTypedefedType()
            if map_deref_type.IsValid():
                self._values = [map.CreateValueFromData(map.name, map.data, map_deref_type)]
            else:
                self._values = [map]
        return False
