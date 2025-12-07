from typing import Union
from lldb import (eBasicTypeLongLong,
                  eBasicTypeUnsignedLongLong,
                  eBasicTypeInt,
                  eBasicTypeUnsignedInt,
                  eBasicTypeChar,
                  eBasicTypeChar16,
                  SBValue,
                  SBData)
from .platformhelpers import platform_is_32bit, get_named_type
from .syntheticstruct import SyntheticStruct
from .qshareddata import QSharedData
from .qarraydatapointer import QArrayDataPointerContainer
from . import qcborvalue


class QCborContainerPrivate(QSharedData):

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)

        bit32 = platform_is_32bit(self._pointer)
        self.add_basic_type_field('used_data', eBasicTypeUnsignedInt if bit32 else eBasicTypeUnsignedLongLong)
        self.add_synthetic_field('data', lambda p: QArrayDataPointerContainer(p, lambda e: e))
        self.add_synthetic_field('elements', lambda p: QArrayDataPointerContainer(p, lambda e: QCborElement(e)))

    def used_data(self) -> SBValue:
        pass

    def data(self) -> QArrayDataPointerContainer[SBValue]:
        pass

    def elements(self) -> QArrayDataPointerContainer['QCborElement']:
        pass

    def byte_data_at(self, index: int) -> Union['ByteData', 'None']:
        element = self.elements().d().element_at(index)
        if not element:
            return None

        if not element.flags().GetValueAsSigned() & QCborElement.VALUE_FLAG_HasByteData:
            return None

        offset = element.value().GetValueAsSigned()
        ref_t = self._pointer.target.GetBasicType(eBasicTypeInt)
        field_name = f'{self._pointer.name}.b_ref'
        b_start = self.data().d().get_ptr().CreateChildAtOffset(field_name, offset, ref_t)
        return ByteData(b_start)

    def value_at(self, index: int) -> 'qcborvalue.QCborValue':
        element = self.elements().d().element_at(index)
        element_flags = element.flags().GetValueAsUnsigned()
        if element_flags & QCborElement.VALUE_FLAG_IsContainer:
            t = self._pointer.target
            d = SBData.CreateDataFromSInt64Array(t.GetByteOrder(), t.GetAddressByteSize(), [-1])
            n = self._pointer.CreateValueFromData('n', d, t.GetBasicType(eBasicTypeLongLong))
            return qcborvalue.QCborValue.from_data(element.type(), n, element.container())
        elif element_flags & QCborElement.VALUE_FLAG_HasByteData:
            t = self._pointer.target
            d = SBData.CreateDataFromSInt64Array(t.GetByteOrder(), t.GetAddressByteSize(), [index])
            n = self._pointer.CreateValueFromData('n', d, t.GetBasicType(eBasicTypeLongLong))
            return qcborvalue.QCborValue.from_data(element.type(), n, self)
        return qcborvalue.QCborValue.from_data(element.type(), element.value())

    def string_data_at(self, index: int) -> Union['SBValue', 'None']:
        data = self.byte_data_at(index)
        if not data:
            return None

        value = data.data()
        elements = self.elements().d().element_at(index)
        if elements.flags().GetValueAsSigned() & QCborElement.VALUE_FLAG_StringIsUtf16:
            data_t = self._pointer.target.GetBasicType(eBasicTypeChar16)
            value = value.CreateValueFromAddress(value.name, value.load_addr, data_t)

        return value


class QCborElement(SyntheticStruct):
    VALUE_FLAG_IsContainer = 0x0001
    VALUE_FLAG_HasByteData = 0x0002
    VALUE_FLAG_StringIsUtf16 = 0x0004
    VALUE_FLAG_StringIsAscii = 0x0008

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_basic_type_field('value', eBasicTypeLongLong)
        self.add_gap_field(-pointer.target.GetBasicType(eBasicTypeLongLong).size)  # emulate a union field
        self.add_synthetic_field_pointer('container', lambda p: QCborContainerPrivate(p))
        self.add_sb_type_field('type', get_named_type(pointer.target, 'QCborValue::Type', eBasicTypeInt))
        self.add_basic_type_field('flags', eBasicTypeInt)

    def pointer(self):
        return self._pointer

    def value(self) -> SBValue:
        pass

    def container(self) -> 'QCborContainerPrivate':
        pass

    def type(self) -> SBValue:
        pass

    def flags(self) -> SBValue:
        pass


class ByteData(SyntheticStruct):

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)

        self.add_basic_type_field('len', eBasicTypeLongLong)
        len = self.len().GetValueAsSigned()
        data_t = pointer.target.GetBasicType(eBasicTypeChar).GetArrayType(len)
        self.add_sb_type_field('data', data_t)

    def len(self) -> SBValue:
        pass

    def data(self) -> SBValue:
        pass
