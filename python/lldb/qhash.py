from abstractsynth import AbstractSynth
from lldb import SBValue, SBType, SBError, eBasicTypeUnsignedLongLong
from helpers import TypeHelpers
import re


def qhash_summary(valobj: SBValue):
    count = valobj.GetChildMemberWithName(QHashSynth.PROP_COUNT).GetValueAsUnsigned()
    return f'count={count}'


class AlignedStruct:
    def __init__(self, t_key: SBType, t_val: SBType):
        self.offset_key = 0
        self.offset_value = self._calc_offset(t_key.size, t_val.size)
        self_min_size = self.offset_value + t_val.size
        self.offset_next = self._calc_offset(self_min_size, self_min_size)

    _alignment = 4  # works for GCCx64; TODO check for MSVC

    @staticmethod
    def _calc_offset(min_offset: int, size: int) -> int:
        if size == 1:
            return min_offset
        _, unaligned_bytes = divmod(min_offset, AlignedStruct._alignment)
        padding = 0 if unaligned_bytes == 0 else AlignedStruct._alignment - unaligned_bytes
        result = min_offset if padding == 0 or padding >= size else min_offset + padding
        return result


class QHashSynth(AbstractSynth):
    PROP_COUNT = 'count'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._type_uint = valobj.GetTarget().GetBasicType(eBasicTypeUnsignedLongLong)
        self._process = valobj.GetProcess()

    def get_child_index(self, name: str) -> int:
        if name == QHashSynth.PROP_COUNT:
            return 0
        else:
            return -1

    def _get_span_size(self) -> int:
        return 128 + 2 * self._type_uint.size

    def _get_key_value_types(self) -> (SBType, SBType, AlignedStruct):
        if self._valobj.type.GetNumberOfTemplateArguments() > 0:
            type_key = self._valobj.type.GetTemplateArgumentType(0)
            type_value = self._valobj.type.GetTemplateArgumentType(1)
        else:
            module = self._valobj.GetFrame().GetModule()
            [type_key, type_value] = TypeHelpers.read_template_types(module, self._valobj.type, 2)

        alignment = AlignedStruct(type_key, type_value)

        return type_key, type_value, alignment

    def _create_key_value(self, address: int, type_key: SBType, type_value: SBType, alignment: AlignedStruct) \
            -> (SBValue, SBValue):
        key = self._valobj.CreateValueFromAddress('k', address + alignment.offset_key, type_key)
        value = self._valobj.CreateValueFromAddress('v', address + alignment.offset_value, type_value)
        return key, value

    def _get_offsets(self, span: int) -> bytearray:
        err = SBError()
        offsets = bytearray(self._process.ReadMemory(span, 128, err))
        if err.Fail():
            print(err.GetCString())
            raise err.GetCString()
        return offsets

    def _get_entries(self, span: int) -> int:
        return self._valobj.CreateValueFromAddress('entries', span + 128, self._type_uint).GetValueAsUnsigned()

    def update(self):
        addr = self._valobj.GetChildMemberWithName('d').GetValueAsUnsigned()
        size = self._valobj.CreateValueFromAddress('count', addr + 8, self._type_uint)
        num_buckets = self._valobj.CreateValueFromAddress('num_buckets', addr + 16,
                                                          self._type_uint).GetValueAsUnsigned()
        spans = self._valobj.CreateValueFromAddress('spans', addr + 32, self._type_uint).GetValueAsUnsigned()
        self._values = [size]

        # print(f'{size} - {num_buckets} - {spans}')

        span_size = self._get_span_size()
        nspans = int((num_buckets + 127) / 128)

        # print(f'span_size={span_size}, nspans={nspans}')

        type_key, type_value, alignment = self._get_key_value_types()

        # print(f'type_key={type_key.name}, type_value={type_value.name}')
        # print(f'key_size={type_key.size}, value_size={type_value.size}')

        for b in range(nspans):
            # print(f'b={b}')
            span = spans + b * span_size
            offsets = self._get_offsets(span)
            entries = self._get_entries(span)

            for i in range(128):
                # print(f'i={i}')
                offset = offsets[i]
                if offset != 255:
                    entry = entries + offset * alignment.offset_next
                    key, value = self._create_key_value(entry, type_key, type_value, alignment)
                    self._values.append(key)
                    self._values.append(value)
        return False


class QHashIteratorSynth(QHashSynth):
    def get_child_index(self, name: str) -> int:
        return -1

    @staticmethod
    def _read_key_type(key_and_value_types: str) -> str:
        n = ''
        t = 0
        for c in key_and_value_types:
            if c == '<':
                t += 1
            if c == '>':
                t -= 1
            if c == ',' and t == 0:
                return n
            n += c
        raise f'Could not read the key type frpm "{key_and_value_types}"'

    def _read_template_param_names(self, type_name: str) -> (str, str):
        args = re.search('<(.+)>', type_name).group(1)
        n_key = self._read_key_type(args)
        n_value = args[len(n_key) + 1:].strip()
        return n_key, n_value

    def _get_key_value_types(self) -> (SBType, SBType, AlignedStruct):
        name_key, name_value = self._read_template_param_names(self._valobj.type.name)

        module = self._valobj.GetFrame().GetModule()
        type_key = module.FindFirstType(name_key)
        type_value = module.FindFirstType(name_value)
        alignment = AlignedStruct(type_key, type_value)

        return type_key, type_value, alignment

    def update(self):
        i = self._valobj.GetChildMemberWithName('i')
        d = i.GetChildMemberWithName('d')
        if not d.value:
            return False  # iterator has ended

        bucket = i.GetChildMemberWithName('bucket').GetValueAsUnsigned()
        spans = d.GetChildMemberWithName('spans').GetValueAsUnsigned()

        # print(f'bucket={bucket}, spans={spans}')

        index_span = int(bucket / 128)
        span = spans + index_span * self._get_span_size()

        # print(f'index_span={index_span}, span={span}')

        offsets = self._get_offsets(span)
        entries = self._get_entries(span)

        # print(offsets)
        # print(f'entries={entries}')

        index_offset = bucket & 127
        offset = offsets[index_offset]
        # print(f'index_offset={index_offset}, offset={offset}')

        type_key, type_value, alignment = self._get_key_value_types()
        entry = entries + offset * alignment.offset_next
        key, value = self._create_key_value(entry, type_key, type_value, alignment)

        self._values = [key, value]

        return False
