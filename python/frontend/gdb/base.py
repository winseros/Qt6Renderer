from typing import Iterable, Tuple
from backend.gdb.native_types import Value
from core import AbstractStructureProvider, AbstractSummaryProvider


class StructureOnlyPrinter:
    def __init__(self, provider: AbstractStructureProvider):
        self._provider = provider

    def children(self) -> Iterable[Tuple[str, Value]]:
        for child in self._provider.iterate_children():
            yield child.get_display_value()

    def display_hint(self):
        return 'array'


class SummaryOnlyPrinter:
    def __init__(self, provider: AbstractSummaryProvider):
        self._provider = provider

    def to_string(self):
        return self._provider.to_string()

    def display_hint(self):
        return 'string'


class StructureAndSummaryPrinter:
    def __init__(self, structure_provider: AbstractStructureProvider, summary_provider: AbstractSummaryProvider):
        self._structure_provider = structure_provider
        self._summary_provider = summary_provider

    def children(self) -> Iterable[Tuple[str, Value]]:
        for child in self._structure_provider.iterate_children():
            yield child.get_display_value()

    def to_string(self):
        return self._summary_provider.to_string()

    def display_hint(self):
        return 'array'
