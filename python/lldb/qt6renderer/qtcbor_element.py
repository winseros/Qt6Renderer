from typing import List
from lldb import SBValue, SBData, eBasicTypeLongLong
from .abstractsynth import AbstractSynth
from .qcborvalue import QCborValue
from .qcborcontainerprivate import QCborElement
from .qcborcontainerprivatesynth import QCborContainerPrivateSynth


def qtcborelement_summaru(valobj: SBValue):
    prop_size = valobj.GetChildMemberWithName(QCborContainerPrivateSynth.PROP_SIZE)
    prop_type = valobj.GetChildMemberWithName(QCborContainerPrivateSynth.PROP_TYPE).GetValueAsSigned()
    if prop_type == QCborValue.TYPE_Map:
        return f'Map, size={prop_size.GetValueAsSigned()}'
    elif prop_type == QCborValue.TYPE_Array:
        return f'Array, size={prop_size.GetValueAsSigned()}'
    return 'Unknown'


class QtCborElementSynth(AbstractSynth):
    def update(self) -> bool:
        element = QCborElement(self._valobj)
        element_type = element.type().GetValueAsSigned()
        self._values: List[SBValue] = []
        if element_type == QCborValue.TYPE_Map:
            synth = QCborContainerPrivateSynth(self._valobj, element.container())
            children = synth.get_children_as_map()
            meta_info = [
                QCborContainerPrivateSynth.get_size_value(self._valobj, len(children) + 2),
                QCborContainerPrivateSynth.get_type_value(element.type())
            ]
            self._values = meta_info + children
            return False
        elif element_type == QCborValue.TYPE_Array:
            synth = QCborContainerPrivateSynth(self._valobj, element.container())
            children = synth.get_children_as_array()
            meta_info = [
                QCborContainerPrivateSynth.get_size_value(self._valobj, len(children) + 2),
                QCborContainerPrivateSynth.get_type_value(element.type())
            ]
            self._values = meta_info + children
            return False

        return True

    def _add_int_value(self, name: str, value: int) -> None:
        target = self._valobj.target
        data_type = target.GetBasicType(eBasicTypeLongLong)
        data = SBData.CreateDataFromSInt64Array(target.GetByteOrder(), target.GetAddressByteSize(), [value])
        self._values.append(self._valobj.CreateValueFromData(name, data, data_type))
