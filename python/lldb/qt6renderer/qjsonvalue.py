from typing import Union

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

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._t_type = valobj.target.FindFirstType('QJsonValue::Type')

    def get_child_index(self, name: str) -> int:
        pass

    def update(self) -> bool:
        cbor_value = QCborValue.from_sb_value(self._valobj)

        self._values.append(
            self._valobj.CreateValueFromData(QJsonValueSynth.PROP_TYPE, self._get_type_data(cbor_value.type()),
                                             self._t_type))

        return False

    def _get_type_data(self, cbor_type: SBValue) -> SBData:
        cbor_type = cbor_type.data.sint32[0]

        if cbor_type == QCborValue.TYPE_Null:
            json_type = QJsonValueSynth.TYPE_Null
        elif cbor_type == QCborValue.TYPE_True or cbor_type == QCborValue.TYPE_False:
            json_type = QJsonValueSynth.TYPE_Bool
        elif cbor_type == QCborValue.TYPE_Double or QCborValue.TYPE_Integer:
            json_type = QJsonValueSynth.TYPE_Double
        elif cbor_type == QCborValue.TYPE_String:
            json_type = QJsonValueSynth.TYPE_String
        elif cbor_type == QCborValue.TYPE_Array:
            json_type = QJsonValueSynth.TYPE_Array
        elif cbor_type == QCborValue.TYPE_Map:
            json_type = QJsonValueSynth.TYPE_Object
        else:
            json_type = QJsonValueSynth.TYPE_Undefined

        tar = self._valobj.target
        json_type_data = SBData.CreateDataFromInt(json_type, tar, tar.GetAddressByteSize(), tar.GetByteOrder())
        return json_type_data
