from .baseprinter import StringOnlyPrinter
from gdb import Value
from typing import List, Union


class QUuidPrinter(StringOnlyPrinter):
    def to_string(self) -> str:
        data1 = QUuidPrinter._to_bytes1(self._valobj['data1'])
        data2 = QUuidPrinter._to_bytes1(self._valobj['data2'])
        data3 = QUuidPrinter._to_bytes1(self._valobj['data3'])
        data4s = self._valobj['data4']
        data4 = QUuidPrinter._to_bytes2(data4s, 0, 2)
        data5 = QUuidPrinter._to_bytes2(data4s, 2)

        result = QUuidPrinter._to_hex(data1) + '-'
        result += QUuidPrinter._to_hex(data2) + '-'
        result += QUuidPrinter._to_hex(data3) + '-'
        result += QUuidPrinter._to_hex(data4) + '-'
        result += QUuidPrinter._to_hex(data5)

        return result

    @staticmethod
    def _to_bytes1(valobj: Value) -> bytes:
        return int(valobj).to_bytes(valobj.type.sizeof, byteorder='big')

    @staticmethod
    def _to_bytes2(valobj: Value, start_at: int, take: int = None) -> List[int]:
        arr = []
        for i in range(start_at, take if take else valobj.type.sizeof):
            arr.append(int(valobj[i]))
        return arr

    @staticmethod
    def _to_hex(data: Union[bytes, List[int]]) -> str:
        result = ''
        for i in range(0, len(data)):
            result += QUuidPrinter._to_letter((data[i] >> 4) & 0x0f)
            result += QUuidPrinter._to_letter(data[i] & 0x0f)

        return result

    @staticmethod
    def _to_letter(number: int) -> str:
        return '0123456789abcdef'[number & 0xF]
