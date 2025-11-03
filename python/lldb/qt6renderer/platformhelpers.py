from lldb import SBValue, SBType


def platform_is_32bit(valobj: SBValue) -> bool:
    pointer_size = valobj.process.GetAddressByteSize()
    return pointer_size == 4


def platform_is_windows(valobj: SBValue) -> bool:
    triple = valobj.target.triple
    windows = triple.find('windows') >= 0
    return windows


def get_pointer_type(valobj: SBValue) -> SBType:
    return valobj.target.FindFirstType('void').GetPointerType()
