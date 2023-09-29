from typing import Iterable, Tuple, Union

from gdb import Value, Type, lookup_type
from .baseprinter import StructureOnlyPrinter


def _lookup_type_safe(type_name: str) -> Union[Type, None]:
    try:
        return lookup_type(type_name)
    except:
        return None


class QLocalePrinter(StructureOnlyPrinter):
    PROP_LANG = 'language'
    PROP_SCRIPT = 'script'
    PROP_TERRITORY = 'territory'
    PROP_RAW_DATA = 'raw_data'

    def children(self) -> Iterable[Tuple[str, Value]]:
        type_name = self._valobj.type.tag

        type_lang = lookup_type(type_name + '::Language')
        type_script = lookup_type(type_name + '::Script')
        type_territory = _lookup_type_safe(type_name + '::Territory')
        if not type_territory:
            type_territory = lookup_type(type_name + '::Country')
        type_num_opts = _lookup_type_safe(type_name + '::NumberOptions')

        d = self._valobj['d']['d'].dereference()
        data = d['m_data'].dereference()

        yield QLocalePrinter.PROP_LANG, data['m_language_id'].cast(type_lang)
        yield QLocalePrinter.PROP_SCRIPT, data['m_script_id'].cast(type_script)
        yield QLocalePrinter.PROP_TERRITORY, data['m_territory_id'].cast(type_territory)
        yield QLocalePrinter.PROP_RAW_DATA, data
