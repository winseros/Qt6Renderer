from lldb import eBasicTypeBool, SBData, SBValue
from .abstractsynth import AbstractSynth


def qbitarray_summary(valobj: SBValue):
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

        target = valobj.GetTarget()
        self._type_bool = target.GetBasicType(eBasicTypeBool)

    def get_child_index(self, name: str) -> int:
        if name == QBitArraySynth.PROP_SIZE:
            return 0
        else:
            index = name.lstrip('[').rstrip(']')
            if index.isdigit():
                return int(index) + QBitArraySynth.RANGE_START_OFFSET
            else:
                return -1

    def update(self) -> bool:
        d_d = self._valobj.GetChildMemberWithName('d').GetChildMemberWithName('d')
        d_d_size = d_d.GetChildMemberWithName(QBitArraySynth.PROP_SIZE)

        self._values.append(d_d_size)

        if d_d_size:
            d_d_size_v = d_d_size.GetValueAsSigned()

            d_d_ptr = d_d.GetChildMemberWithName('ptr')
            d_d_bytes = d_d_ptr.GetPointeeData(0, d_d_size_v).sint8s
            # if not data.IsValid()

            d_bits_val = (d_d_size_v << 3) - d_d_bytes[
                0]  # the 1st byte represents the number of unused bits in the last byte

            if d_bits_val:
                bit_index_global = 0
                for byte_index in range(1, len(d_d_bytes)):
                    byte = d_d_bytes[byte_index]
                    bit_index_in_byte = 0
                    while bit_index_in_byte < 8 and bit_index_global < d_bits_val:
                        bit = 0x01 & (byte >> bit_index_in_byte)

                        data = SBData.CreateDataFromInt(bit)
                        bit_val = self._valobj.CreateValueFromData(f'[{bit_index_global}]', data, self._type_bool)
                        self._values.append(bit_val)

                        bit_index_in_byte += 1
                        bit_index_global += 1

            return False
