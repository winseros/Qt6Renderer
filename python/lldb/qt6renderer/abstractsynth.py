from lldb import SBValue
from abc import abstractmethod


class AbstractSynth:
    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._values = []

    def has_children(self) -> bool:
        return len(self._values) > 0

    def num_children(self) -> int:
        return len(self._values)

    def get_child_at_index(self, index: int) -> SBValue:
        return self._values[index] if index < len(self._values) else None

    @abstractmethod
    def get_child_index(self, name: str) -> int: ...

    @abstractmethod
    def update(self) -> bool: ...

    def get_value(self):
        return self._valobj
