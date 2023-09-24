from typing import Tuple, Iterable
from abc import abstractmethod
from gdb import Value


class AbstractPrinter:
    def __init__(self, valobj: Value):
        self._valobj = valobj


class StringOnlyPrinter(AbstractPrinter):
    @abstractmethod
    def to_string(self) -> str:
        pass

    def display_hint(self):
        return 'string'


class StructureOnlyPrinter(AbstractPrinter):
    @abstractmethod
    def children(self) -> Iterable[Tuple[str, Value]]:
        pass


class StringAndStructurePrinter(AbstractPrinter):
    @abstractmethod
    def to_string(self) -> str:
        pass

    @abstractmethod
    def children(self) -> Iterable[Tuple[str, Value]]:
        pass
