from lldb import SBValue, SBType, eBasicTypeInt, eBasicTypeLongLong


def platform_is_32bit(valobj: SBValue) -> bool:
    pointer_size = valobj.process.GetAddressByteSize()
    return pointer_size == 4


def platform_is_windows(valobj: SBValue) -> bool:
    triple = valobj.target.triple
    windows = triple.find('windows') >= 0
    return windows


def get_void_pointer_type(valobj: SBValue) -> SBType:
    # note for future myself
    # void pointer is convenient to use for SyntheticStruct debugging
    return valobj.target.FindFirstType('void').GetPointerType()


def get_int_pointer_type(valobj: SBValue) -> SBType:
    # note for future myself
    # int pointer is convenient to use when need to dereference
    return valobj.target.GetBasicType(eBasicTypeInt if platform_is_32bit(valobj) else eBasicTypeLongLong).GetPointerType()
