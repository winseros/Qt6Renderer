from lldb import SBValue, SBType, eBasicTypeInt
from math import ceil
from typing import Union, Callable
from .platformhelpers import get_void_pointer_type


class SyntheticStruct:
    def __init__(self, pointer: SBValue):
        self._pointer = pointer
        self._size = 0

    def add_gap_field(self, gap_size: int):
        self._size += gap_size

    def add_basic_type_field(self, name: str, basic_type: int, pointer=False, getter_name: str = None):
        sb_type = self._pointer.GetTarget().GetBasicType(basic_type)
        if pointer:
            sb_type = sb_type.GetPointerType()
        self._add_field(name, sb_type, getter_name)

    def add_named_type_field(self, name: str, type_name: str, getter_name: str = None):
        sb_type = self._pointer.GetTarget().FindFirstType(type_name)
        self._add_field(name, sb_type, getter_name)

    def add_sb_type_field(self, name: str, sb_type: SBType, getter_name: str = None):
        self._add_field(name, sb_type, getter_name)

    def add_synthetic_field(self, name: str, synthetic_struct_ctor: Callable[[SBValue], 'SyntheticStruct']):
        synthetic_struct = synthetic_struct_ctor(self._pointer)
        field_byte_offset = self._get_field_byte_offset(synthetic_struct)

        if field_byte_offset:
            field_name = f'{self._pointer.name}.{name}.{field_byte_offset}_{synthetic_struct.size}'
            field_ref = self._get_field_ref(field_name, field_byte_offset,
                                            self._pointer.target.GetBasicType(eBasicTypeInt))
            synthetic_struct = synthetic_struct_ctor(field_ref)

        self._size = field_byte_offset + synthetic_struct.size

        setattr(self, name, lambda: synthetic_struct)

    def add_synthetic_field_pointer(self, name: str, synthetic_struct_ctor: Callable[[SBValue], 'SyntheticStruct']):
        ptr_t = get_void_pointer_type(self._pointer)

        field_byte_offset = self._get_field_byte_offset(ptr_t)
        field_name = f'{self._pointer.name}.{name}.{field_byte_offset}_{ptr_t.size}-ptr'
        field_ref = self._get_field_ref(field_name, field_byte_offset, ptr_t)
        synthetic_struct = synthetic_struct_ctor(field_ref)

        self._size = field_byte_offset + ptr_t.size

        setattr(self, name, lambda: synthetic_struct)

    def _add_field(self, name: str, type: SBType, getter_name: str):
        if not getter_name:
            getter_name = name

        byte_offset = self._get_field_byte_offset(type)
        self._size = byte_offset + type.size
        setattr(self, getter_name, lambda: self._field_impl(name, byte_offset, type))

    def _field_impl(self, name: str, byte_offset: int, type: SBType) -> SBValue:
        val = self._get_field_ref(name, byte_offset, type)
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

    def _get_load_addr(self) -> int:
        return self._pointer.GetValueAsUnsigned() if self._pointer.TypeIsPointerType() else self._pointer.load_addr

    def _get_field_ref(self, name: str, byte_offset: int, type: SBType) -> SBValue:
        addr = self._get_load_addr()
        ref = self._pointer.CreateValueFromAddress(name, addr + byte_offset, type)
        return ref

    @property
    def size(self):
        # the property name "size" must match the SBType "size" property name
        return self._size

    def get_sibling_aligned_size(self):
        sibling_offset = self._get_field_byte_offset(self)
        return sibling_offset
