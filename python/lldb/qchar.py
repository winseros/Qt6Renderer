from lldb import SBValue, SBError


def qchar_summary(valobj: SBValue):
    data = valobj.GetData()
    error = SBError()
    value = data.GetUnsignedInt16(error, 0)
    if error.Success():
        return 'u\'{}\' ({})'.format(chr(value), value)

    print('qchar_summary: ' + error.GetCString())
    return None
