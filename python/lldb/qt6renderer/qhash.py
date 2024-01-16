from lldb import SBData, SBType, SBValue, eBasicTypeBool, eBasicTypeUnsignedLongLong, eBasicTypeInt
from .abstractsynth import AbstractSynth
from .typehelpers import TypeHelpers
from .syntheticstruct import SyntheticStruct


def qhash_summary(valobj: SBValue) -> str:
    size = valobj.GetChildMemberWithName(QHashSynth.PROP_SIZE).GetValueAsUnsigned()
    return f'size={size}'


class QHashSynth(AbstractSynth):
    PROP_SIZE = 'size'

    def get_child_index(self, name: str) -> int:
        if name == QHashSynth.PROP_SIZE:
            return 0
        else:
            return -1

    def update(self) -> bool:
        d = self._valobj.GetChildMemberWithName('d')
        if not d.GetValueAsUnsigned():
            sb_type = self._valobj.target.GetBasicType(eBasicTypeUnsignedLongLong)
            sb_data = SBData.CreateDataFromInt(0)
            self._values = [self._valobj.CreateValueFromData(QHashSynth.PROP_SIZE, sb_data, sb_type)]
            return False

        size = d.GetChildMemberWithName(QHashSynth.PROP_SIZE)
        self._values = [size]

        num_buckets = d.GetChildMemberWithName('numBuckets').GetValueAsUnsigned()

        nspans = int((num_buckets + 127) / 128)
        p_span = d.GetChildMemberWithName('spans')

        [t_key, t_value] = TypeHelpers.get_template_types(self._valobj.type, 2, self._valobj.target)
        entry_size = KeyValuePair(self._valobj, t_key, t_value).get_sibling_aligned_size()

        sb_int = self._valobj.target.GetBasicType(eBasicTypeInt)

        for b in range(nspans):
            span = self._valobj.CreateValueFromAddress('span', p_span.load_addr + b * p_span.size,
                                                       p_span.type).Dereference()

            offsets = span.GetChildMemberWithName('offsets').data.uint8s
            entries_addr = span.GetChildMemberWithName('entries').GetValueAsUnsigned()

            for i in range(128):
                offset = offsets[i]
                if offset != 255:
                    sb_pair = self._valobj.CreateValueFromAddress('pair', entries_addr + offset * entry_size, sb_int)
                    pair = KeyValuePair(sb_pair, t_key, t_value)

                    self._values.append(pair.k())
                    self._values.append(pair.v())

        return False


class QHashIteratorSynth(AbstractSynth):
    PROP_K = 'k'
    PROP_V = 'v'
    PROP_END = 'end'

    def get_child_index(self, name: str) -> int:
        if self.num_children() == 2:
            if name == QHashIteratorSynth.PROP_K:
                return 0
            elif name == QHashIteratorSynth.PROP_V:
                return 1
        elif self.num_children() == 1:
            if name == QHashIteratorSynth.PROP_END:
                return 0
        return -1

    def update(self) -> bool:
        i = self._valobj.GetChildMemberWithName('i')
        d = i.GetChildMemberWithName('d')
        if not d.GetValueAsUnsigned():
            sb_type = self._valobj.target.GetBasicType(eBasicTypeBool)
            sb_data = SBData.CreateDataFromInt(1)
            self._values = [self._valobj.CreateValueFromData(QHashIteratorSynth.PROP_END, sb_data, sb_type)]
            return False  # iterator has ended

        [t_key, t_value] = TypeHelpers.get_template_types(self._valobj.type, 2, self._valobj.target)

        entry_size = KeyValuePair(self._valobj, t_key, t_value).get_sibling_aligned_size()
        sb_int = self._valobj.target.GetBasicType(eBasicTypeInt)

        bucket = i.GetChildMemberWithName('bucket').GetValueAsUnsigned()
        p_span = d.GetChildMemberWithName('spans')

        index_span = int(bucket / 128)
        span = self._valobj.CreateValueFromAddress('span', p_span.load_addr + index_span * p_span.size,
                                                   p_span.type).Dereference()

        index_offset = bucket & 127
        offsets = span.GetChildMemberWithName('offsets').data.uint8s
        entries_addr = span.GetChildMemberWithName('entries').GetValueAsUnsigned()

        sb_pair = self._valobj.CreateValueFromAddress('pair', entries_addr + offsets[index_offset] * entry_size, sb_int)
        pair = KeyValuePair(sb_pair, t_key, t_value)

        self._values = [pair.k(), pair.v()]


class KeyValuePair(SyntheticStruct):
    def __init__(self, pointer: SBValue, t_key: SBType, t_value: SBType):
        super().__init__(pointer)
        self.add_sb_type_field('k', t_key)
        self.add_sb_type_field('v', t_value)

    def k(self) -> SBValue:
        pass

    def v(self) -> SBValue:
        pass
