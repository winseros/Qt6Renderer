from lldb import SBValue


def qchar_summary(valobj: SBValue):
    val = valobj.data.uint16[0]
    return f'u\'{chr(val)}\' ({val})'
