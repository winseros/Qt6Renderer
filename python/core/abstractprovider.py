from abc import ABCMeta, abstractmethod
from backend.abstract import AbstractValue
from typing import Iterable


class AbstractSummaryProvider(metaclass=ABCMeta):
    def __init__(self, value: AbstractValue):
        self._value = value

    @abstractmethod
    def to_string(self) -> str:
        pass


class AbstractStructureProvider(metaclass=ABCMeta):
    def __init__(self, value: AbstractValue):
        self._value = value
        self._children: list[AbstractValue] = []

    def has_children(self) -> bool:
        return len(self._children) > 0

    def get_child_count(self) -> int:
        return len(self._children)

    def get_child_at_index(self, index: int) -> AbstractValue:
        return self._children[index]

    @abstractmethod
    def get_child_index(self, child_name: str) -> int:
        pass

    @abstractmethod
    def iterate_children(self) -> Iterable[AbstractValue]:
        pass

    def update(self):
        self._children = list(self.iterate_children())
