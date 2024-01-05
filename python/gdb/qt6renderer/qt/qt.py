from gdb import parse_and_eval, lookup_symbol, Value
from enum import IntEnum
from typing import Union


class QtVersion(IntEnum):
    V6_0_0 = 0x060000
    V6_4_0 = 0x060400


class QtTiVersion(IntEnum):
    V22 = 22


class Qt:
    def version(self) -> int:
        # Only available with Qt 5.3+
        qt_version = int(parse_and_eval('*(&qtHookData)')[2])
        self.version = lambda: qt_version
        return qt_version

    def symbol_address(self, symbolName) -> Value:
        res = parse_and_eval('(qsizetype*)' + symbolName)
        return None if res is None else res

    def qt_hook_data_symbol_name(self) -> str:
        return 'qtHookData'

    def type_info_version(self) -> Union[int, None]:
        addr = self.symbol_address(self.qt_hook_data_symbol_name())
        if addr:
            # Only available with Qt 5.3+
            hook_version = addr.dereference()
            if hook_version >= 3:
                ti_version = int((addr + 6).dereference())
                self.type_info_version = lambda: ti_version
                return ti_version
        return None


qt_instance__ = Qt()


def qt() -> Qt:
    return qt_instance__
