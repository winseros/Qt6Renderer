from lldb import SBValue, SBType
from math import ceil


class SyntheticStruct:
    def __init__(self, pointer: SBValue):
        self._pointer = pointer
        self._size = 0

    def add_field(self, name: str, type: int, pointer=False):
        # if not name in vars(self):
        #     raise Exception(f'The placeholder for the property \'{name}\' must exist')

        sb_type = self._pointer.GetTarget().GetBasicType(type)
        if pointer:
            sb_type = sb_type.GetPointerType()

        byte_offset = self._get_field_byte_offset(sb_type)
        self._size = byte_offset + sb_type.size
        setattr(self, name, lambda: self._field_impl(name, byte_offset, sb_type))

    def _field_impl(self, name: str, byte_offset: int, type: SBType) -> SBValue:
        load_addr = self._pointer.GetValueAsUnsigned() + byte_offset
        val = self._pointer.CreateValueFromAddress(name, load_addr, type)
        setattr(self, name, lambda: val)
        return val

    def _get_field_byte_offset(self, type: SBType) -> int:
        alignment = self._get_field_byte_alignment(type)
        offset = ceil(self._size / alignment) * alignment
        return offset

    def _get_field_byte_alignment(self, type: SBType) -> int:
        pointer_size = self._pointer.GetTarget().GetAddressByteSize()
        if type.size >= pointer_size:
            return pointer_size

        alignment = 1
        while type.size > alignment:
            alignment *= 2

        return alignment
