from lldb import SBValue, SBError


def qatomicint_summary(valobj: SBValue):
    data = valobj.GetData()
    error = SBError()
    value = data.GetSignedInt32(error, 0)
    if error.Success():
        return str(value)

    return None
