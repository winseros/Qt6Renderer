from lldb import SBValue
from abc import abstractmethod
from typing import Union, List


class AbstractSynth:
    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._values: List[SBValue] = []

    def has_children(self) -> bool:
        return True

    def num_children(self) -> int:
        return len(self._values)

    def get_child_at_index(self, index: int) -> Union[SBValue, None]:
        return self._values[index] if index < len(self._values) else None

    def get_child_index(self, name: str) -> int:
        for index, value in enumerate(self._values):
            if name == value.name:
                return index
        return -1

    @abstractmethod
    def update(self) -> bool: ...

    def get_value(self):
        return self._valobj
