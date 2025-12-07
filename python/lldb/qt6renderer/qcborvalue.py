from typing import Union
from lldb import eBasicTypeInt, eBasicTypeLongLong, SBValue

from .abstractsynth import AbstractSynth
from .syntheticstruct import SyntheticStruct
from .platformhelpers import get_named_type
from . import qcborcontainerprivate


class QCborValueSynth(AbstractSynth):
    PROP_TYPE = 'type'
    PROP_VALUE = 'value'

    def get_child_index(self, name: str) -> int:
        if name == QCborValueSynth.PROP_TYPE:
            return 0
        else:
            return -1

    def update(self) -> bool:
        val = QCborValue.from_sb_value(self._valobj)

        self._values = [self._valobj.CreateValueFromData(QCborValueSynth.PROP_TYPE, val.type().data, val.type().type)]

        sb_value = val.get_value()
        if sb_value:
            self._values.append(sb_value)

        return False


class QCborValue(SyntheticStruct):
    SIMPLE_TYPE_False = 20
    SIMPLE_TYPE_True = 21
    SIMPLE_TYPE_Null = 22
    SIMPLE_TYPE_Undefined = 23

    TYPE_Integer = 0x00
    TYPE_ByteArray = 0x40
    TYPE_String = 0x60
    TYPE_Array = 0x80
    TYPE_Map = 0xa0
    TYPE_Tag = 0xc0

    # range 0x100 - 0x1ff for Simple Types
    TYPE_SimpleType = 0x100
    TYPE_False = TYPE_SimpleType + SIMPLE_TYPE_False
    TYPE_True = TYPE_SimpleType + SIMPLE_TYPE_True
    TYPE_Null = TYPE_SimpleType + SIMPLE_TYPE_Null
    TYPE_Undefined = TYPE_SimpleType + SIMPLE_TYPE_Undefined

    TYPE_Double = 0x202

    # extended (tagged) types
    TYPE_DateTime = 0x10000
    TYPE_Url = 0x10020
    TYPE_RegularExpression = 0x10023
    TYPE_Uuid = 0x10025

    TYPE_Invalid = -1

    @staticmethod
    def from_sb_value(pointer: SBValue) -> 'QCborValue':
        cbor = QCborValue(pointer)
        cbor.add_basic_type_field('n', eBasicTypeLongLong)
        cbor.add_synthetic_field_pointer('container', lambda p: qcborcontainerprivate.QCborContainerPrivate(p))
        cbor.add_sb_type_field('type', get_named_type(pointer.target, 'QCborValue::Type', eBasicTypeInt))
        return cbor

    @staticmethod
    def from_data(type: SBValue, n: SBValue, container: Union[qcborcontainerprivate.QCborContainerPrivate, None] = None) -> 'QCborValue':
        cbor = QCborValue(None)
        cbor.n = lambda: n
        cbor.container = lambda: container
        cbor.type = lambda: type
        return cbor

    def get_value(self) -> Union[SBValue, None]:
        data_type = self.type().data.sint32[0]
        if data_type in [QCborValue.TYPE_Integer, QCborValue.TYPE_Double]:
            return self.n()
        elif data_type == QCborValue.TYPE_ByteArray:
            byte_data = self.container().byte_data_at(self.n().GetValueAsSigned())
            if byte_data:
                return byte_data.data()
        elif data_type == QCborValue.TYPE_String:
            string_data = self.container().string_data_at(self.n().GetValueAsSigned())
            if string_data:
                return string_data
        elif data_type in [QCborValue.TYPE_DateTime, QCborValue.TYPE_Url, QCborValue.TYPE_RegularExpression]:
            string_data = self.container().string_data_at(1)
            if string_data:
                return string_data
        elif data_type == QCborValue.TYPE_Uuid:
            byte_data = self.container().byte_data_at(1)
            if byte_data:
                return byte_data.data()

        return None

    def n(self) -> SBValue:
        pass

    def container(self) -> 'qcborcontainerprivate.QCborContainerPrivate':
        pass

    def type(self) -> SBValue:
        pass
