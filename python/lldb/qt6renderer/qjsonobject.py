from typing import List
from lldb import SBData, SBValue, eBasicTypeLongLong, eBasicTypeBool, eBasicTypeDouble, \
    eBasicTypeNullPtr
from .abstractsynth import AbstractSynth
from .platformhelpers import get_pointer_type
from .qcborcontainerprivate import QCborContainerPrivate
from .qcborvalue import QCborValue


class QJsonObjectSynth(AbstractSynth):
    PROP_SIZE = 'size'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._cbor_element_type = None

    def get_child_index(self, name: str) -> int:
        for index, value in self._values:
            if name == value.name:
                return index
        return -1

    def update(self) -> bool:
        t_pointer = get_pointer_type(self._valobj)
        pointer = self._valobj.CreateValueFromAddress('ptr', self._valobj.load_addr, t_pointer)

        self._values: List[SBValue] = []

        if pointer.GetValueAsUnsigned():
            container = QCborContainerPrivate(pointer)
            size = int(container.elements().d().get_size().GetValueAsSigned() / 2)
            self._add_int_value(self.PROP_SIZE, size)

            for i in range(0, size):
                name = container.string_data_at(i * 2)
                name_str = self._get_string(name)

                self._add_cbor_value(name_str, container, i * 2 + 1)
        else:
            self._add_int_value(self.PROP_SIZE, 0)

        return False

    def _add_cbor_value(self, name: str, container: QCborContainerPrivate, index: int):
        element = container.elements().d().element_at(index)
        element_type = element.type().GetValueAsSigned()
        if (element_type in [QCborValue.TYPE_Integer, QCborValue.TYPE_String,
                             QCborValue.TYPE_Url, QCborValue.TYPE_DateTime, QCborValue.TYPE_RegularExpression,
                             QCborValue.TYPE_Uuid, QCborValue.TYPE_ByteArray]):
            cbor = container.value_at(index)
            self._add_sb_value(name, cbor.get_value())
        elif element_type == QCborValue.TYPE_Double:
            cbor = container.value_at(index)
            self._add_double_value(name, cbor.get_value())
        elif element_type == QCborValue.TYPE_False:
            self._add_bool_value(name, False)
        elif element_type == QCborValue.TYPE_True:
            self._add_bool_value(name, True)
        elif element_type == QCborValue.TYPE_Null:
            self._add_null_value(name)
        elif element_type == QCborValue.TYPE_Map or element_type == QCborValue.TYPE_Array:
            self._add_container_value(name, element.pointer())

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

    def _add_null_value(self, name: str) -> None:
        data_type = self._valobj.target.GetBasicType(eBasicTypeNullPtr)
        data = SBData.CreateDataFromInt(0)
        self._values.append(self._valobj.CreateValueFromData(name, data, data_type))

    def _add_container_value(self, name: str, reference: SBValue) -> None:
        if not self._cbor_element_type:
            self._cbor_element_type = self._valobj.target.FindFirstType('QtCbor::Element')
        if not self._cbor_element_type:
            print(f'Could not render the json object property: {name}')
            return
        prop = self._valobj.CreateValueFromAddress(name, reference.load_addr, self._cbor_element_type)
        self._values.append(prop)

    @staticmethod
    def _get_string(value: SBValue) -> str:
        text = ''
        for char in value.data.sint8:
            text += chr(char)
        return text
