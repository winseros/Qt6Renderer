from lldb import SBValue, eBasicTypeUnsignedLongLong
from .platformhelpers import get_int_pointer_type, get_void_pointer_type
from .abstractsynth import AbstractSynth
from .syntheticstruct import SyntheticStruct
from .qcborcontainerprivate import QCborContainerPrivate
from .qcborcontainerprivatesynth import QCborContainerPrivateSynth
from .qcborvalue import QCborValue


def qjsonvalueconstref_summary(valobj: SBValue) -> str:
    element_type = valobj.GetChildMemberWithName(QjsonValueConstRefSynth.PROP_TYPE).GetValueAsSigned()
    if element_type == QCborValue.TYPE_Map:
        value = valobj.GetChildMemberWithName(QjsonValueConstRefSynth.PROP_VALUE)
        size = value.GetChildMemberWithName(QCborContainerPrivateSynth.PROP_SIZE)
        return f'Map, size={size.GetValueAsSigned()}'
    elif element_type == QCborValue.TYPE_Array:
        value = valobj.GetChildMemberWithName(QjsonValueConstRefSynth.PROP_VALUE)
        size = value.GetChildMemberWithName(QCborContainerPrivateSynth.PROP_SIZE)
        return f'Array, size={size.GetValueAsSigned()}'
    elif element_type == QCborValue.TYPE_Null:
        return 'Null'
    else:
        value = valobj.GetChildMemberWithName(QjsonValueConstRefSynth.PROP_VALUE)
        return value.GetValue()


class QjsonValueConstRef(SyntheticStruct):

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_sb_type_field('d', get_int_pointer_type(pointer))
        self.add_basic_type_field('flags', eBasicTypeUnsignedLongLong)

    def d(self) -> SBValue:
        pass

    def flags(self) -> SBValue:
        pass


class QjsonValueConstRefSynth(AbstractSynth):
    PROP_TYPE = 'type'
    PROP_VALUE = 'value'

    def update(self) -> bool:
        self._values = []

        struct = QjsonValueConstRef(self._valobj)

        array_or_obj_ptr = struct.d().Dereference()
        container_ptr = self._valobj.CreateValueFromAddress('ptr', array_or_obj_ptr.load_addr,
                                                            get_void_pointer_type(self._valobj))
        flags = struct.flags().GetValueAsUnsigned()
        is_object = flags & 0x01
        index = flags >> 1

        if is_object:
            index = index * 2 + 1

        container = QCborContainerPrivate(container_ptr)
        container_element_type = container.elements().d().element_at(index).type()

        synth = QCborContainerPrivateSynth(self._valobj, container)
        value = synth.get_index_value(self.PROP_VALUE, container, index)
        value_type = self._valobj.CreateValueFromData(self.PROP_TYPE, container_element_type.data,
                                                      container_element_type.type)
        self._values = [value_type, value]

        return False
