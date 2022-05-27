from lldb import SBValue, SBData, SBError, eBasicTypeLongLong, eBasicTypeBool
from abstractsynth import AbstractSynth


def qbitarray_summary(valobj):
    # type: (SBValue) -> str
    """Formats the QT QBitArray type"""
    child_count = valobj.GetNumChildren()
    if child_count == 1:
        return ''

    text = ''
    for i in range(0, child_count - QBitArraySynth.RANGE_START_OFFSET):
        child = valobj.GetChildAtIndex(i + QBitArraySynth.RANGE_START_OFFSET)
        bit_value = child.GetValueAsUnsigned()
        if i and not i % 4:
            text += ' '
        text += '1' if bit_value else '0'

    return text


class QBitArraySynth(AbstractSynth):
    PROP_SIZE = 'size'
    RANGE_START_OFFSET = 1

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)

        process = valobj.GetProcess()
        self._endianness = process.GetByteOrder()
        self._pointer_size = process.GetAddressByteSize()
        target = valobj.GetTarget()
        self._type_long_long = target.GetBasicType(eBasicTypeLongLong)
        self._type_bool = target.GetBasicType(eBasicTypeBool)

        size_data_zero = SBData.CreateDataFromSInt64Array(self._endianness, self._pointer_size, [0])
        self._values_zero = [
            valobj.CreateValueFromData(self.PROP_SIZE, size_data_zero, self._type_long_long)
        ]

    def has_children(self) -> bool:
        return True

    def get_child_index(self, name: str) -> int:
        if name == QBitArraySynth.PROP_SIZE:
            return 0
        else:
            index = name.lstrip('[').rstrip(']')
            if index.isdigit():
                return int(index) + QBitArraySynth.RANGE_START_OFFSET
            else:
                return -1

    def update(self):
        self._values = self._values_zero

        d_d = self._valobj.GetChildMemberWithName('d').GetChildMemberWithName('d')
        d_d_size_val = d_d.GetChildMemberWithName('size').GetValueAsUnsigned()
        if d_d_size_val:
            d_d_ptr_val = d_d.GetChildMemberWithName('ptr').GetValueAsUnsigned()
            error = SBError()
            d_d_bytes = self._valobj.GetProcess().ReadMemory(d_d_ptr_val, d_d_size_val, error)
            if error.Success():
                d_d_bytes_val = bytearray(d_d_bytes)
                d_bits_val = (d_d_size_val << 3) - d_d_bytes_val[
                    0]  # the 1st byte represents the number of unused bits in the last byte
                if d_bits_val:
                    size_data = SBData.CreateDataFromSInt64Array(self._endianness, self._pointer_size, [d_bits_val])
                    self._values = [
                        self._valobj.CreateValueFromData(QBitArraySynth.PROP_SIZE, size_data, self._type_long_long)
                    ]

                    bit_index_global = 0
                    for byte_index in range(1, len(d_d_bytes_val)):
                        byte = d_d_bytes_val[byte_index]
                        bit_index_in_byte = 0
                        while bit_index_in_byte < 8 and bit_index_global < d_bits_val:
                            bit = (byte >> bit_index_in_byte) & 0x01

                            bit_data = SBData.CreateDataFromSInt32Array(self._endianness, self._pointer_size, [bit])
                            bit_value = self._valobj.CreateValueFromData('[%s]' % bit_index_global, bit_data,
                                                                         self._type_bool)
                            self._values.append(bit_value)

                            bit_index_in_byte += 1
                            bit_index_global += 1
            else:
                print('QBitArraySynth: ' + error.GetCString())

        return False
