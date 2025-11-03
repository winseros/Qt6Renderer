from .abstractsynth import AbstractSynth
from .qcborcontainerprivate import QCborContainerPrivate, QCborElement
from .qcborvalue import QCborValue
from .platformhelpers import get_pointer_type
from typing import Union
from lldb import SBData, SBValue, eBasicTypeChar, eBasicTypeLongLong, eBasicTypeBool, eBasicTypeDouble, \
    eBasicTypeNullPtr


class QJsonObjectSynth(AbstractSynth):
    PROP_SIZE = 'size'

    def get_child_index(self, name: str) -> int:
        if name == self.PROP_SIZE:
            return 0
        else:
            return -1

    def update(self) -> bool:
        t_pointer = get_pointer_type(self._valobj)
        pointer = self._valobj.CreateValueFromAddress('ptr', self._valobj.load_addr, t_pointer)

        self._values = []

        if pointer.GetValueAsUnsigned():
            container = QCborContainerPrivate(pointer)
            size = int(container.elements().d().get_size().GetValueAsSigned() / 2)
            self._add_int_value(self.PROP_SIZE, size)

            for i in range(0, size):
                name = container.string_data_at(i * 2)
                name_str = self._get_string(name)

                cbor = container.value_at(i * 2 + 1)
                self._add_cbor_value(name_str, cbor)
        else:
            self._add_int_value(self.PROP_SIZE, 0)

        return False

    def _add_cbor_value(self, name: str, cbor: QCborValue):
        element_type = cbor.type().GetValueAsSigned()
        if (element_type in [QCborValue.TYPE_Integer, QCborValue.TYPE_String,
                             QCborValue.TYPE_Url, QCborValue.TYPE_DateTime, QCborValue.TYPE_RegularExpression,
                             QCborValue.TYPE_Uuid, QCborValue.TYPE_ByteArray]):
            self._add_sb_value(name, cbor.get_value())
        elif element_type == QCborValue.TYPE_Double:
            self._add_double_value(name, cbor.get_value())
        elif element_type == QCborValue.TYPE_False:
            self._add_bool_value(name, False)
        elif element_type == QCborValue.TYPE_True:
            self._add_bool_value(name, True)
        elif element_type == QCborValue.TYPE_Null:
            self._add_null_value(name)

    def _add_bool_value(self, name: str, value: bool) -> None:
        data_type = self._valobj.target.GetBasicType(eBasicTypeBool)
        data = SBData.CreateDataFromInt(value)
        self._values.append(self._valobj.CreateValueFromData(name, data, data_type))

    def _add_sb_value(self, name: str, value: SBValue) -> None:

        self._values.append(self._valobj.CreateValueFromAddress(name, value.load_addr, value.type))
        #self._values.append(self._valobj.CreateValueFromData(name, value.data, value.type))

    def _add_int_value(self, name: str, value: int) -> None:
        target = self._valobj.target
        data_type = target.GetBasicType(eBasicTypeLongLong)
        data = SBData.CreateDataFromSInt64Array(target.GetByteOrder(), target.GetAddressByteSize(), [value])
        self._values.append(self._valobj.CreateValueFromData(name, data, data_type))

    def _add_double_value(self, name: str, value: SBValue) -> None:
        data_type = self._valobj.target.GetBasicType(eBasicTypeDouble)
        self._values.append(self._valobj.CreateValueFromData(name, value.GetData(), data_type))

    def _add_null_value(self, name: str) -> None:
        data_type = self._valobj.target.GetBasicType(eBasicTypeNullPtr)
        data = SBData.CreateDataFromInt(0)
        self._values.append(self._valobj.CreateValueFromData(name, data, data_type))

    @staticmethod
    def _get_string(value: SBValue) -> str:
        text = ''
        for char in value.data.sint8:
            text += chr(char)
        return text
