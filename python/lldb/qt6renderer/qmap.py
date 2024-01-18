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
            self._values = [d_d.GetChildMemberWithName('m')]
        return False
