from lldb import SBValue
from typing import List


def quuid_summary(valobj: SBValue):
    data1 = valobj.GetChildMemberWithName('data1').data.uint8s
    data2 = valobj.GetChildMemberWithName('data2').data.uint8s
    data3 = valobj.GetChildMemberWithName('data3').data.uint8s
    data4 = valobj.GetChildMemberWithName('data4').data.uint8s

    result = _to_hex(data1, reverse=True) + '-'
    result += _to_hex(data2, reverse=True) + '-'
    result += _to_hex(data3, reverse=True) + '-'
    result += _to_hex(data4[0:2]) + '-'
    result += _to_hex(data4[2:])

    return result


def quuid_summary_from_byte_array(valobj: SBValue) -> str:
    data = valobj.data.sint8
    data4 = data[8:16]

    result = _to_hex(data[0:4]) + '-'
    result += _to_hex(data[4:6]) + '-'
    result += _to_hex(data[6:8]) + '-'
    result += _to_hex(data4[0:2]) + '-'
    result += _to_hex(data4[2:])

    return result


def _to_hex(data: List[int], reverse=False) -> str:
    result = ''

    if reverse:
        for i in range(len(data), 0, -1):
            result += _to_letter((data[i - 1] >> 4) & 0x0f)
            result += _to_letter(data[i - 1] & 0x0f)
    else:
        for i in range(0, len(data)):
            result += _to_letter((data[i] >> 4) & 0x0f)
            result += _to_letter(data[i] & 0x0f)

    return result


def _to_letter(number: int) -> str:
    return '0123456789abcdef'[number & 0xF]
