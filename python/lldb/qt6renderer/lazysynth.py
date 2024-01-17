from lldb import SBValue
from abc import abstractmethod
from typing import Tuple, Union, Dict

from .abstractsynth import AbstractSynth


class LazySynth(AbstractSynth):

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._num_children = 0
        self._values: Dict[int, SBValue] = dict()

    def num_children(self) -> int:
        return self._num_children

    def get_child_at_index(self, index: int) -> Union[SBValue, None]:
        if index > self._num_children:
            return None

        value = self._values.get(index, None)
        if not value:
            value = self._fetch_child_at_index(index)
            self._values[index] = value

        return value

    @abstractmethod
    def _fetch_child_at_index(self, index: int) -> SBValue:
        ...
