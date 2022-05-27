from lldb import SBValue, SBError, eBasicTypeUnsignedInt, eBasicTypeSignedChar
from qstring import qstring_summary
from helpers import QtHelpers
from abstractsynth import AbstractSynth

def qhostaddress_summary(valobj: SBValue):
    type_char = valobj.GetTarget().GetBasicType(eBasicTypeSignedChar)
    addr = valobj.GetChildMemberWithName('d').GetChildMemberWithName('d').GetValueAsUnsigned()
    protocol = valobj.CreateValueFromAddress('p', addr + 52, type_char).GetValueAsUnsigned()

    text = '(Invalid)'
    if protocol == 0:
        text = _format_as_v4(valobj, addr)
    elif protocol == 1:
        text = _format_as_v6(valobj, addr)
    return text

def _format_as_v4(valobj: SBValue, addr: int) -> str:
    type_uint = valobj.GetTarget().GetBasicType(eBasicTypeUnsignedInt)
    a4 = valobj.CreateValueFromAddress('a4', addr + 48, type_uint).GetValueAsUnsigned()

    a4, n4 = divmod(a4, 256)
    a4, n3 = divmod(a4, 256)
    a4, n2 = divmod(a4, 256)
    a4, n1 = divmod(a4, 256)

    return f'{n1}.{n2}.{n3}.{n4}'

def _format_as_v6(valobj: SBValue, addr: int) -> str:
    err = SBError()
    a6 = valobj.GetProcess().ReadMemory(addr + 32, 16, err)
    if err.Fail():
        return err.GetCString()
    a6 = bytearray(a6)

    text = ''
    for i in range(0, len(a6), 2):
        if i > 0:
            text += ':'
        text += f'{a6[i]:02x}{a6[i + 1]:02x}'
    return text