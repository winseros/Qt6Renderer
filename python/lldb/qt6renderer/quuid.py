from lldb import SBValue, SBError


def quuid_summary(valobj: SBValue):
    data1 = _get_bytes1(valobj.GetChildMemberWithName('data1'))
    data2 = _get_bytes1(valobj.GetChildMemberWithName('data2'))
    data3 = _get_bytes1(valobj.GetChildMemberWithName('data3'))
    data4 = _get_bytes2(valobj.GetChildMemberWithName('data4'))

    result = _to_hex(data1) + '-'
    result += _to_hex(data2) + '-'
    result += _to_hex(data3) + '-'
    result += _to_hex(data4[0:2]) + '-'
    result += _to_hex(data4[2:])

    return result


def _get_bytes1(val: SBValue) -> bytes:
    return val.GetValueAsUnsigned().to_bytes(val.size, byteorder='big')


def _get_bytes2(val: SBValue) -> bytes:
    data = val.data.uint8s
    return bytes(data)


def _to_hex(data: bytes) -> str:
    result = ''
    for i in range(0, len(data)):
        result += _to_letter((data[i] >> 4) & 0x0f)
        result += _to_letter(data[i] & 0x0f)

    return result


def _to_letter(number: int) -> str:
    return '0123456789abcdef'[number & 0xF]
