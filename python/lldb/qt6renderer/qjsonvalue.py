from lldb import eBasicTypeDouble, eBasicTypeBool, eBasicTypeLongLong, eBasicTypeNullPtr

from lldb import SBValue, SBData
from .abstractsynth import AbstractSynth
from .qcborvalue import QCborValue


def qjsonvalue_summary(valobj):
    pass


class QJsonValueSynth(AbstractSynth):
    PROP_TYPE = 'Type'
    PROP_VALUE = 'Value'
    PROP_SIZE = 'Size'
    PROP_RAW = 'RawData'

    TYPE_Null = 0x0
    TYPE_Bool = 0x1
    TYPE_Double = 0x2
    TYPE_String = 0x3
    TYPE_Array = 0x4
    TYPE_Object = 0x5
    TYPE_Undefined = 0x80

    def get_child_index(self, name: str) -> int:
        num_children = self.num_children()

        if name == self.PROP_TYPE:
            return 0
        elif num_children > 1 and name == self.PROP_VALUE:
            return 1

        return -1

    def update(self) -> bool:
        cbor_value = QCborValue.from_sb_value(self._valobj)

        self._add_json_type(self.PROP_TYPE, cbor_value.type())
        self._add_cbor_value(cbor_value)

        return False

    def _add_cbor_value(self, cbor: QCborValue):
        element_type = cbor.type().GetValueAsSigned()
        if (element_type in [QCborValue.TYPE_Integer, QCborValue.TYPE_String,
                             QCborValue.TYPE_Url, QCborValue.TYPE_DateTime, QCborValue.TYPE_RegularExpression,
                             QCborValue.TYPE_Uuid, QCborValue.TYPE_ByteArray]):
            self._add_sb_value(self.PROP_VALUE, cbor.get_value())
        elif element_type == QCborValue.TYPE_Double:
            self._add_double_value(self.PROP_VALUE, cbor.get_value())
        elif element_type == QCborValue.TYPE_False:
            self._add_bool_value(self.PROP_VALUE, False)
        elif element_type == QCborValue.TYPE_True:
            self._add_bool_value(self.PROP_VALUE, True)
        elif element_type == QCborValue.TYPE_Null:
            pass

    def _add_bool_value(self, name: str, value: bool) -> None:
        data_type = self._valobj.target.GetBasicType(eBasicTypeBool)
        data = SBData.CreateDataFromInt(value)
        self._values.append(self._valobj.CreateValueFromData(name, data, data_type))

    def _add_sb_value(self, name: str, value: SBValue) -> None:
        self._values.append(self._valobj.CreateValueFromAddress(name, value.load_addr, value.type))

    def _add_int_value(self, name: str, value: int) -> None:
        target = self._valobj.target
        data_type = target.GetBasicType(eBasicTypeLongLong)
        data = SBData.CreateDataFromSInt64Array(target.GetByteOrder(), target.GetAddressByteSize(), [value])
        self._values.append(self._valobj.CreateValueFromData(name, data, data_type))

    def _add_double_value(self, name: str, value: SBValue) -> None:
        data_type = self._valobj.target.GetBasicType(eBasicTypeDouble)
        self._values.append(self._valobj.CreateValueFromData(name, value.GetData(), data_type))

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
