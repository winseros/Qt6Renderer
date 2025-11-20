from lldb import SBValue, SBData, SBType, eBasicTypeLongLong, eBasicTypeDouble, eBasicTypeBool, eBasicTypeNullPtr
from typing import List, Union
from .qcborcontainerprivate import QCborContainerPrivate
from .qcborvalue import QCborValue


class QCborContainerPrivateSynth:
    PROP_SIZE = 'size'
    PROP_TYPE = 'type'

    def __init__(self, valobj: SBValue, container: QCborContainerPrivate):
        self._valobj = valobj
        self._container = container
        self._cbor_element_type: Union[SBType, None] = None

    @staticmethod
    def get_size_value(valobj: SBValue, size: int) -> SBValue:
        target = valobj.target
        data_type = target.GetBasicType(eBasicTypeLongLong)
        data = SBData.CreateDataFromSInt64Array(target.GetByteOrder(), target.GetAddressByteSize(), [size])
        return valobj.CreateValueFromData(QCborContainerPrivateSynth.PROP_SIZE, data, data_type)

    @staticmethod
    def get_type_value(type: SBValue):
        return type.CreateValueFromAddress(QCborContainerPrivateSynth.PROP_TYPE, type.load_addr, type.type)

    def get_children_as_map(self) -> List[SBValue]:
        num_children = self._container.elements().d().get_size().GetValueAsSigned()

        children: List[SBValue] = []

        for i in range(0, num_children, 2):
            name = self._container.string_data_at(i)
            name_str = self._get_string(name)

            child = self._get_index_value(name_str, self._container, i + 1)
            if child:
                children.append(child)

        return children

    def get_children_as_array(self) -> List[SBValue]:
        num_children = self._container.elements().d().get_size().GetValueAsSigned()

        children: List[SBValue] = []

        for i in range(0, num_children):
            child = self._get_index_value(f'[{i}]', self._container, i)
            if child:
                children.append(child)

        return children

    def _get_index_value(self, name: str, container: QCborContainerPrivate, index: int) -> Union[SBValue, None]:
        element = container.elements().d().element_at(index)
        element_type = element.type().GetValueAsSigned()
        if (element_type in [QCborValue.TYPE_Integer, QCborValue.TYPE_String,
                             QCborValue.TYPE_Url, QCborValue.TYPE_DateTime, QCborValue.TYPE_RegularExpression,
                             QCborValue.TYPE_Uuid, QCborValue.TYPE_ByteArray]):
            cbor = container.value_at(index)
            return self._get_sb_value(name, cbor.get_value())
        elif element_type == QCborValue.TYPE_Double:
            cbor = container.value_at(index)
            return self._get_double_value(name, cbor.get_value())
        elif element_type == QCborValue.TYPE_False:
            return self._get_bool_value(name, False)
        elif element_type == QCborValue.TYPE_True:
            return self._get_bool_value(name, True)
        elif element_type == QCborValue.TYPE_Null:
            return self._add_null_value(name)
        elif element_type == QCborValue.TYPE_Map or element_type == QCborValue.TYPE_Array:
            return self._get_container_value(name, element.pointer())

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

    def _get_container_value(self, name: str, reference: SBValue) -> Union[SBValue, None]:
        if not self._cbor_element_type:
            self._cbor_element_type = self._valobj.target.FindFirstType('QtCbor::Element')
        if not self._cbor_element_type:
            print(f'Could not render the json object property: {name}')
            return
        container_prop = self._valobj.CreateValueFromAddress(name, reference.load_addr, self._cbor_element_type)
        return container_prop

    @staticmethod
    def _get_string(value: SBValue) -> str:
        text = ''
        for char in value.data.sint8:
            text += chr(char)
        return text
