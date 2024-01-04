from typing import Iterable, Tuple

from gdb import Value, Type, lookup_type
from .baseprinter import StructureOnlyPrinter


class QVariantPrinter(StructureOnlyPrinter):
    PROP_VALUE = 'value'
    PROP_TYPE_NAME = 'typeName'

    _builtins_a = ['bool', 'int', 'unsigned int', 'long long', 'unsigned long long', 'double']
    _builtins_d = ['long', 'short', 'char', 'unsigned long', 'unsigned short', 'unsigned char', 'float']

    def children(self) -> Iterable[Tuple[str, Value]]:
        d = self._valobj['d']
        p_data = d['packedType'] << 2

        t_uint = lookup_type('unsigned int')
        type_id = (p_data.cast(t_uint.pointer()) + 3).dereference()

        value = None
        if 0 < type_id <= 6:
            value = self._internal(d, self._builtins_a[type_id - 1])
        elif type_id == 31:
            value = self._void_star(d)
        elif 32 <= type_id <= 38:
            value = self._internal(d, self._builtins_d[type_id - 32])
        elif type_id == 40:
            value = self._internal(d, 'char')
        else:
            value = self._external(d, p_data)

        if value:
            yield QVariantPrinter.PROP_VALUE, value
        else:
            for prop in self._default(d, p_data):
                yield prop

    @staticmethod
    def _void_star(d: Value):
        t = lookup_type('void').pointer()
        value = d.cast(t)
        return value

    @staticmethod
    def _internal(d: Value, type_name: str) -> Value:
        t = lookup_type(type_name)
        value = d.cast(t)
        return value

    def _external(self, d: Value, p_data: Value) -> Value:
        t_value = QVariantPrinter._lookup_type(p_data)

        is_shared = bool(d['is_shared'])
        if is_shared:
            t_value = t_value.pointer()

        value = d.cast(t_value)

        if is_shared:
            value = value.dereference()

        return value

    @staticmethod
    def _lookup_type(p_data: Value) -> Type:
        p_char = lookup_type('char').pointer().pointer()
        p_type_name = p_data.reinterpret_cast(p_char) + 3

        type_name = p_type_name.dereference().string('', 'replace')
        type = lookup_type(type_name)
        return type

    @staticmethod
    def _default(d: Value, p_data: Value) -> Tuple[str, Value]:
        t_value = QVariantPrinter._lookup_type(p_data)
        yield QVariantPrinter.PROP_TYPE_NAME, t_value.name

        for field in d.type.fields():
            yield field.name, d[field.name]
