from typing import Iterable

from backend.abstract import AbstractValue
from .abstractprovider import AbstractStructureProvider


class QArayDataPointerStructureProvider(AbstractStructureProvider):

    def get_child_index(self, child_name: str) -> int:
        return 0

    def iterate_children(self) -> Iterable[AbstractValue]:
        d = self._value.get_child('d')
        d.display_name = 'raw_data'

        d_size = d.get_child('size')
        d_size.display_name = 'size'
        yield d_size

        d_d = d.get_child('d')
        d_d_alloc = d_d.get_child('alloc')
        d_d_alloc.display_name = 'capacity'
        yield d_d_alloc

        yield d

        d_ptr = d.get_child('ptr')
        for i in range(d_size.get_python_value()):
            data_value = d_ptr.get_pointer_value(i)
            data_value.display_name = f'[{i}]'
            yield data_value
