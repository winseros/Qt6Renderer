from lldb import SBValue, SBType
from math import ceil
from typing import Union


class SyntheticStruct:
    def __init__(self, pointer: SBValue):
        self._pointer = pointer
        self._size = 0
        self._byte_offset = 0

    def add_basic_type_field(self, name: str, basic_type: int, pointer=False):
        sb_type = self._pointer.GetTarget().GetBasicType(basic_type)
        if pointer:
            sb_type = sb_type.GetPointerType()
        self._add_field(name, sb_type)

    def add_named_type_field(self, name: str, type_name: str):
        sb_type = self._pointer.GetTarget().FindFirstType(type_name)
        self._add_field(name, sb_type)

    def add_synthetic_field(self, name: str, synthetic_struct: 'SyntheticStruct'):
        assert name in dir(self)

        byte_offset = self._get_field_byte_offset(synthetic_struct)
        synthetic_struct._byte_offset = byte_offset
        
        self._size = byte_offset + synthetic_struct.size
        setattr(self, name, lambda: synthetic_struct)

    def _add_field(self, name: str, type: SBType):
        assert name in dir(self)

        byte_offset = self._get_field_byte_offset(type)
        self._size = byte_offset + type.size
        setattr(self, name, lambda: self._field_impl(name, byte_offset, type))

    def _field_impl(self, name: str, byte_offset: int, type: SBType) -> SBValue:
        load_addr = self._pointer.GetValueAsUnsigned() + self._byte_offset + byte_offset
        val = self._pointer.CreateValueFromAddress(name, load_addr, type)
        setattr(self, name, lambda: val)
        return val

    def _get_field_byte_offset(self, type: Union[SBType, 'SyntheticStruct']) -> int:
        alignment = self._get_field_byte_alignment(type)
        offset = ceil(self._size / alignment) * alignment
        return offset

    def _get_field_byte_alignment(self, type: Union[SBType, 'SyntheticStruct']) -> int:
        pointer_size = self._pointer.GetTarget().GetAddressByteSize()
        if type.size >= pointer_size:
            return pointer_size

        alignment = 1
        while type.size > alignment:
            alignment *= 2

        return alignment

    @property
    def size(self):
        return self._size
