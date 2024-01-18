from lldb import SBValue, SBType, eBasicTypeInt
from math import ceil
from typing import Union, Callable


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

    def add_synthetic_field(self, name: str, synthetic_struct_ctor: Callable[[SBValue], 'SyntheticStruct'],
                            pointer=False):
        if pointer:
            sb_ptr_t = self._pointer.target.GetBasicType(eBasicTypeInt).GetPointerType()

            field_byte_offset = self._get_field_byte_offset(sb_ptr_t)
            field_addr = self._get_struct_addr()
            struct_ptr = self._pointer.CreateValueFromAddress(name, field_addr + field_byte_offset, sb_ptr_t)
            synthetic_struct = synthetic_struct_ctor(struct_ptr)

            self._size = field_byte_offset + sb_ptr_t.size
        else:
            synthetic_struct = synthetic_struct_ctor(self._pointer)
            field_byte_offset = self._get_field_byte_offset(synthetic_struct)

            if field_byte_offset:
                sb_int = self._pointer.target.GetBasicType(eBasicTypeInt)
                sb_field_name = f'{self._pointer.name}.{hex(field_byte_offset)}'
                struct_addr = self._get_struct_addr()
                sb_pointer = self._pointer.CreateValueFromAddress(sb_field_name, struct_addr + field_byte_offset,
                                                                  sb_int)
                synthetic_struct = synthetic_struct_ctor(sb_pointer)

            self._size = field_byte_offset + synthetic_struct.size

        setattr(self, name, lambda: synthetic_struct)

    def _add_field(self, name: str, type: SBType, getter_name: str):
        if not getter_name:
            getter_name = name

        byte_offset = self._get_field_byte_offset(type)
        self._size = byte_offset + type.size
        setattr(self, getter_name, lambda: self._field_impl(name, byte_offset, type))

    def _field_impl(self, name: str, byte_offset: int, type: SBType) -> SBValue:
        struct_addr = self._get_struct_addr()

        field_addr = struct_addr + byte_offset

        val = self._pointer.CreateValueFromAddress(name, field_addr, type)
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

    def _get_struct_addr(self) -> int:
        struct_addr = self._pointer.GetValueAsUnsigned() if self._pointer.TypeIsPointerType() else self._pointer.load_addr
        return struct_addr

    @property
    def size(self):
        return self._size

    def get_sibling_aligned_size(self):
        sibling_offset = self._get_field_byte_offset(self)
        return sibling_offset
