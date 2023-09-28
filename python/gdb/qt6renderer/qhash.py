from typing import Iterable, Tuple

from gdb import Value, Type, lookup_type
from math import ceil
from .baseprinter import StringAndStructurePrinter, StructureOnlyPrinter


def _get_key_value_types(type: Type) -> Tuple[Type, Type, int]:
    type_key = type.template_argument(0)
    type_value = type.template_argument(1)
    a_value = _get_value_byte_alignment(type_key, type_value)
    return type_key.pointer(), type_value.pointer(), a_value


def _get_value_byte_alignment(t_key: Type, t_value: Type) -> int:
    a_value = t_value.alignof
    s_key = t_key.sizeof

    div = ceil(s_key / a_value)
    offset = div * a_value
    return offset


class QHashPrinter(StringAndStructurePrinter):
    def to_string(self) -> str:
        d = self._valobj['d'].dereference()
        size = d['size']
        return f'size={size}'

    def children(self) -> Iterable[Tuple[str, Value]]:
        p_type_key, p_type_value, v_alignment = _get_key_value_types(self._valobj.type)
        t_char = lookup_type('char').pointer()

        d = self._valobj['d'].dereference()

        num_buckets = int(d['numBuckets'])
        nspans = int((num_buckets + 127) / 128)
        p_span = d['spans']

        for b in range(nspans):
            span = (p_span + b).dereference()
            offsets = span['offsets']
            entries = span['entries']

            for i in range(128):
                offset = offsets[i]
                if offset != 255:
                    p_key = (entries + offset).reinterpret_cast(p_type_key)
                    p_value = (p_key.cast(t_char) + v_alignment).reinterpret_cast(p_type_value)

                    yield f'k{i}', p_key.dereference()
                    yield f'v{i}', p_value.dereference()

    def display_hint(self):
        return 'map'


class QHashIteratorPrinter(StructureOnlyPrinter):
    PROP_END = 'end'

    def children(self) -> Iterable[Tuple[str, Value]]:
        i = self._valobj['i']
        d = i['d']
        if not d:
            yield QHashIteratorPrinter.PROP_END, True
            return

        parent_type = QHashIteratorPrinter._get_parent_type(self._valobj.type)
        p_type_key, p_type_value, v_alignment = _get_key_value_types(parent_type)
        t_char = lookup_type('char').pointer()

        d = d.dereference()

        bucket = int(i['bucket'])
        index_span = int(bucket / 128)
        index_offset = bucket & 127

        span = (d['spans'] + index_span).dereference()
        offsets = span['offsets']
        entries = span['entries']

        offset = offsets[index_offset]

        p_key = (entries + offset).reinterpret_cast(p_type_key)
        p_value = (p_key.cast(t_char) + v_alignment).reinterpret_cast(p_type_value)

        yield 'k', p_key.dereference()
        yield 'v', p_value.dereference()

    @staticmethod
    def _get_parent_type(iterator_type: Type) -> Type:
        parent_type_name = iterator_type.name.split('::')[0]
        parent_type = lookup_type(parent_type_name)
        return parent_type
