from .abstractsynth import AbstractSynth
from .qcborvalue import QCborValue
from .qcborcontainerprivate import QCborElement

class QtCborElementSynth(AbstractSynth):

    def get_child_index(self, name: str) -> int:
        return 0

    def update(self) -> bool:
        element = QCborElement(self._valobj)
        print(hex(element.type().GetValueAsSigned()))

        return False
