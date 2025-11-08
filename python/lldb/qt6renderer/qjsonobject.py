from typing import List
from lldb import SBValue
from .abstractsynth import AbstractSynth
from .platformhelpers import get_pointer_type
from .qcborcontainerprivate import QCborContainerPrivate
from .qcborcontainerprivatesynth import QCborContainerPrivateSynth


class QJsonObjectSynth(AbstractSynth):
    def update(self) -> bool:
        t_pointer = get_pointer_type(self._valobj)
        pointer = self._valobj.CreateValueFromAddress('ptr', self._valobj.load_addr, t_pointer)

        self._values: List[SBValue] = []

        if pointer.GetValueAsUnsigned():
            container = QCborContainerPrivate(pointer)
            synth = QCborContainerPrivateSynth(self._valobj, container)
            children = synth.get_children_as_map()

            self._values = [QCborContainerPrivateSynth.get_size_value(self._valobj, len(children) + 1)] + children
        else:
            self._values = [QCborContainerPrivateSynth.get_size_value(self._valobj, 0)]

        return False
