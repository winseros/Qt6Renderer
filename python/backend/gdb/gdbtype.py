from backend.abstract.abstracttype import AbstractType
from backend.gdb.native_types import Type


class GdbType(AbstractType):
    def __init__(self, native_type: Type):
        self._type = native_type

    def get_pointer_type(self) -> 'GdbType':
        return GdbType(self._type.pointer())

    def get_reference_type(self) -> 'GdbType':
        return GdbType(self._type.reference())

    def get_target_type(self) -> 'GdbType':
        return GdbType(self._type.target())

    def get_name(self) -> str:
        return self._type.tag if self._type.tag else self._type.name

    def get_size(self) -> int:
        return self._type.sizeof

    @property
    def native_type(self):
        return self._type
