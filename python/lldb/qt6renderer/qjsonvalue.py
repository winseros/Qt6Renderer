from typing import Union, List
from lldb import eBasicTypeDouble, eBasicTypeBool, eBasicTypeLongLong, eBasicTypeNullPtr, eBasicTypeChar

from lldb import SBValue, SBData
from .abstractsynth import AbstractSynth
from .qcborvalue import QCborValue
from .qcborcontainerprivatesynth import QCborContainerPrivateSynth


def qjsonvalue_summary(valobj: SBValue) -> str:
    type = valobj.GetChildMemberWithName(QJsonValueSynth.PROP_TYPE).GetValueAsSigned()
    if type == QJsonValueSynth.TYPE_Null:
        return 'Null'
    if type == QJsonValueSynth.TYPE_Bool:
        value = valobj.GetChildMemberWithName(QJsonValueSynth.PROP_VALUE).GetValueAsSigned()
        return 'True' if value else 'False'
    if type == QJsonValueSynth.TYPE_Double:
        value = valobj.GetChildMemberWithName(QJsonValueSynth.PROP_VALUE).GetValue()
        return value
    if type == QJsonValueSynth.TYPE_String:
        txt = ''
        value = valobj.GetChildMemberWithName(QJsonValueSynth.PROP_VALUE)
        chars = value.data.sint8 if value.type.GetArrayElementType() == valobj.target.GetBasicType(
            eBasicTypeChar) else value.data.sint16
        for char in chars:
            txt += chr(char)
        return txt
    if type == QJsonValueSynth.TYPE_Array:
        size = valobj.GetChildMemberWithName(QCborContainerPrivateSynth.PROP_SIZE).GetValueAsSigned()
        return f'Array, size={size}'
    if type == QJsonValueSynth.TYPE_Object:
        size = valobj.GetChildMemberWithName(QCborContainerPrivateSynth.PROP_SIZE).GetValueAsSigned()
        return f'Object, size={size}'
    return '<Undefined>'


class QJsonValueSynth(AbstractSynth):
    PROP_TYPE = 'type'
    PROP_VALUE = 'value'

    TYPE_Null = 0x0
    TYPE_Bool = 0x1
    TYPE_Double = 0x2
    TYPE_String = 0x3
    TYPE_Array = 0x4
    TYPE_Object = 0x5
    TYPE_Undefined = 0x80

    def update(self) -> bool:
        cbor_value = QCborValue.from_sb_value(self._valobj)

        self._values = []
        self._add_json_type(self.PROP_TYPE, cbor_value.type())
        self._add_cbor_value(self.PROP_VALUE, cbor_value)

        return False

    def _add_cbor_value(self, name: str, cbor: QCborValue) -> None:
        values = self._get_cbor_value(name, cbor)
        for value in values:
            self._values.append(value)

    def _get_cbor_value(self, name: str, cbor: QCborValue) -> List[SBValue]:
        element_type = cbor.type().GetValueAsSigned()
        if (element_type in [QCborValue.TYPE_Integer, QCborValue.TYPE_String,
                             QCborValue.TYPE_Url, QCborValue.TYPE_DateTime, QCborValue.TYPE_RegularExpression,
                             QCborValue.TYPE_Uuid, QCborValue.TYPE_ByteArray]):
            return [self._get_sb_value(name, cbor.get_value())]
        elif element_type == QCborValue.TYPE_Double:
            return [self._get_double_value(name, cbor.get_value())]
        elif element_type == QCborValue.TYPE_False:
            return [self._get_bool_value(name, False)]
        elif element_type == QCborValue.TYPE_True:
            return [self._get_bool_value(name, True)]
        elif element_type == QCborValue.TYPE_Null:
            return [self._add_null_value(name)]
        elif element_type == QCborValue.TYPE_Map:
            values = QCborContainerPrivateSynth(self._valobj, cbor.container()).get_children_as_map()
            size = QCborContainerPrivateSynth.get_size_value(self._valobj, len(values))
            return [size] + values
        elif element_type == QCborValue.TYPE_Array:
            values = QCborContainerPrivateSynth(self._valobj, cbor.container()).get_children_as_array()
            size = QCborContainerPrivateSynth.get_size_value(self._valobj, len(values))
            return [size] + values

    def _get_bool_value(self, name: str, value: bool) -> SBValue:
        data_type = self._valobj.target.GetBasicType(eBasicTypeBool)
        data = SBData.CreateDataFromInt(value)
        return self._valobj.CreateValueFromData(name, data, data_type)

    def _get_sb_value(self, name: str, value: SBValue) -> SBValue:
        return self._valobj.CreateValueFromAddress(name, value.load_addr, value.type)

    def _add_int_value(self, name: str, value: int) -> SBValue:
        target = self._valobj.target
        data_type = target.GetBasicType(eBasicTypeLongLong)
        data = SBData.CreateDataFromSInt64Array(target.GetByteOrder(), target.GetAddressByteSize(), [value])
        return self._valobj.CreateValueFromData(name, data, data_type)

    def _get_double_value(self, name: str, value: SBValue) -> SBValue:
        data_type = self._valobj.target.GetBasicType(eBasicTypeDouble)
        return self._valobj.CreateValueFromData(name, value.GetData(), data_type)

    def _add_null_value(self, name: str) -> SBValue:
        data_type = self._valobj.target.GetBasicType(eBasicTypeNullPtr)
        data = SBData.CreateDataFromInt(0)
        return self._valobj.CreateValueFromData(name, data, data_type)

    def _add_json_type(self, name: str, cbor_type: SBValue) -> None:
        cbor_type = cbor_type.GetValueAsSigned()

        if cbor_type == QCborValue.TYPE_Null:
            json_type = QJsonValueSynth.TYPE_Null
        elif cbor_type == QCborValue.TYPE_True or cbor_type == QCborValue.TYPE_False:
            json_type = QJsonValueSynth.TYPE_Bool
        elif cbor_type == QCborValue.TYPE_Double or cbor_type == QCborValue.TYPE_Integer:
            json_type = QJsonValueSynth.TYPE_Double
        elif cbor_type == QCborValue.TYPE_String:
            json_type = QJsonValueSynth.TYPE_String
        elif cbor_type == QCborValue.TYPE_Array:
            json_type = QJsonValueSynth.TYPE_Array
        elif cbor_type == QCborValue.TYPE_Map:
            json_type = QJsonValueSynth.TYPE_Object
        else:
            json_type = QJsonValueSynth.TYPE_Undefined

        t_json_type = self._valobj.target.FindFirstType('QJsonValue::Type')
        sb_value = self._valobj.CreateValueFromData(name, self._valobj.data.CreateDataFromInt(json_type), t_json_type)
        self._values.append(sb_value)
