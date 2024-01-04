from .baseprinter import StringAndStructurePrinter
from gdb import lookup_type


class QBitArrayPrinter(StringAndStructurePrinter):
    PROP_SIZE = 'size'

    def to_string(self) -> str:
        d_d = self._valobj['d']['d']
        d_d_size = d_d['size']
        return f'{QBitArrayPrinter.PROP_SIZE}={str(d_d_size)}'

    def children(self):
        d_d = self._valobj['d']['d']
        d_d_size = d_d['size']
        if d_d_size:
            d_d_ptr = d_d['ptr']

            d_d_bytes = []
            for i in range(d_d_size):
                d_d_bytes.append(d_d_ptr.dereference())
                d_d_ptr += 1

            d_bits_val = (d_d_size << 3) - d_d_bytes[
                0]  # the 1st byte represents the number of unused bits in the last byte

            if d_bits_val:
                bit_index_global = 0
                type_char = lookup_type('char')
                for byte_index in range(1, len(d_d_bytes)):
                    byte = d_d_bytes[byte_index]
                    bit_index_in_byte = 0
                    while bit_index_in_byte < 8 and bit_index_global < d_bits_val:
                        bit = 0x01 & (byte >> bit_index_in_byte)

                        bit_data = bit.cast(type_char)
                        yield (f'[{bit_index_global}]', bit_data)

                        bit_index_in_byte += 1
                        bit_index_global += 1
        else:
            yield QBitArrayPrinter.PROP_SIZE, 0
