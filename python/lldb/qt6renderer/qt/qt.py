import lldb
from enum import IntEnum
from typing import Union


class QtVersion(IntEnum):
    V6_0_0 = 0x060000
    V6_4_0 = 0x060400
    V6_6_0 = 0x060600


class QtTiVersion(IntEnum):
    V22 = 22


class Qt:
    def version(self) -> Union[int, None]:
        # Only available with Qt 5.3+
        hook_data = lldb.target.FindFirstGlobalVariable('qtHookData')
        if not hook_data.IsValid():
            return None

        qt_version = hook_data.GetPointeeData(2, 1).uint64s[0]
        self.version = lambda: qt_version
        return qt_version


qt_instance__ = Qt()


def qt() -> Qt:
    return qt_instance__
