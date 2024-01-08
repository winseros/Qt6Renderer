from lldb import SBValue


def platform_is_32bit(valobj: SBValue) -> bool:
    pointer_size = valobj.process.GetAddressByteSize()
    return pointer_size == 4


def platform_is_windows(valobj: SBValue) -> bool:
    triple = valobj.target.triple
    windows = triple.find('windows') >= 0
    return windows
