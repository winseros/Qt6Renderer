from backend.abstract.abstractvalue import AbstractValue
from backend.abstract.abstracttype import AbstractType
from .native_types import Value
from .gdbtype import GdbType


class GdbValue(AbstractValue):
    def __init__(self, value: Value, display_name: str = None):
        super().__init__(display_name)
        self._value = value

    def get_type(self) -> GdbType:
        return GdbType(self._value.type)

    def get_child(self, name: str) -> 'GdbValue':
        return GdbValue(self._value[name])

    def get_pointer_value(self, offset: int = 0, type: AbstractType = None) -> 'GdbValue':
        val = self._value
        if offset:
            val = self._value + offset
        if type:
            val = val.cast(type.native_type)
        val = val.dereference()
        return GdbValue(val)

    @property
    def native_value(self) -> Value:
        return self._value

    def get_display_value(self):
        if not self.display_name:
            raise Exception('display_name must be set')
        return (self.display_name, self._value)

    def get_python_value(self) -> int:
        return self._value
