from lldb import SBValue, eBasicTypeInt, eBasicTypeLongLong, eBasicTypeChar, eBasicTypeUnsignedInt
from .syntheticstruct import SyntheticStruct
from .abstractsynth import AbstractSynth
from .qcborvalue import QCborValue
from .qcborcontainerprivatesynth import QCborContainerPrivateSynth
from .platformhelpers import get_void_pointer_type, get_named_type


def qjsondocument_summary(valobj: SBValue):
    prop_size = valobj.GetChildMemberWithName(QCborContainerPrivateSynth.PROP_SIZE)
    prop_type = valobj.GetChildMemberWithName(QJsonDocumentSynth.PROP_TYPE).GetValueAsSigned()

    if prop_type == QCborValue.TYPE_Map:
        return f'Map, size={prop_size.GetValueAsSigned()}'
    elif prop_type == QCborValue.TYPE_Array:
        return f'Array, size={prop_size.GetValueAsSigned()}'
    elif prop_type == QCborValue.TYPE_Null:
        return f'Empty'
    return 'Unknown'


class QJsonDocumentPrivate(SyntheticStruct):

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_synthetic_field('value', lambda p: QCborValue.from_sb_value(p))
        type_char_ptr = pointer.target.GetBasicType(eBasicTypeChar).GetPointerType()
        self.add_sb_type_field('raw_data', type_char_ptr)
        self.add_basic_type_field('raw_data_size', eBasicTypeUnsignedInt)

    def value(self) -> QCborValue:
        pass

    def raw_data(self) -> SBValue:
        pass

    def raw_data_size(self) -> SBValue:
        pass


class QJsonDocumentSynth(AbstractSynth):
    PROP_TYPE = 'type'
    PROP_RAW_DATA = 'raw_data'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._t_size = valobj.target.GetBasicType(eBasicTypeLongLong)
        self._t_type = get_named_type(valobj.target, 'QCborValue::Type', eBasicTypeInt)

    def update(self) -> bool:
        self._values = []

        d = self._valobj.GetChildMemberWithName('d')
        if not d.IsValid():
            return False

        pointer = self._valobj.CreateValueFromAddress('ptr', d.load_addr, get_void_pointer_type(self._valobj))
        if not pointer.GetValueAsSigned():
            data = self._valobj.data.CreateDataFromInt(QCborValue.TYPE_Null)
            self._values = [self._valobj.CreateValueFromData(QJsonDocumentSynth.PROP_TYPE, data, self._t_type)]
            return False

        private = QJsonDocumentPrivate(pointer)
        cbor_value = private.value()
        cbor_type = cbor_value.type()

        self._values.append(
            self._valobj.CreateValueFromData(QJsonDocumentSynth.PROP_TYPE, cbor_type.data, cbor_type.type))

        cbor_type_int = cbor_type.GetValueAsSigned()
        if cbor_type_int == QCborValue.TYPE_Map:
            values = QCborContainerPrivateSynth(self._valobj, cbor_value.container()).get_children_as_map()
            size = QCborContainerPrivateSynth.get_size_value(self._valobj, len(values))
            self._values.append(size)
            self._values += values
        elif cbor_type_int == QCborValue.TYPE_Array:
            values = QCborContainerPrivateSynth(self._valobj, cbor_value.container()).get_children_as_array()
            size = QCborContainerPrivateSynth.get_size_value(self._valobj, len(values))
            self._values.append(size)
            self._values += values

        return False
