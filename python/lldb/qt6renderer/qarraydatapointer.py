from lldb import SBValue, SBData, eBasicTypeUnsignedLongLong
from .lazysynth import LazySynth


class QArrayDataPointerSynth(LazySynth):
    # the provider layout is:
    # [size]
    # [capacity]
    # [raw_data]
    # [0..n]

    PROP_SIZE = 'size'
    PROP_CAPACITY = 'capacity'
    PROP_RAW_DATA = 'raw_data'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._num_data_fields = 0

    def get_child_index(self, name: str) -> int:
        if name == self.PROP_SIZE:
            return 0
        elif self._num_data_fields > 0 and name == self.PROP_CAPACITY:
            return 1
        elif self._num_data_fields > 1 and name == self.PROP_RAW_DATA:
            return 2
        elif self._num_data_fields > 2:
            index = name.lstrip('[').rstrip(']')
            if index.isdigit():
                return int(index) + self._num_data_fields

        return -1

    def _fetch_child_at_index(self, index: int) -> SBValue:
        d = self._valobj.GetChildMemberWithName('d')
        d_ptr = d.GetChildMemberWithName('ptr')

        addr = d_ptr.GetValueAsUnsigned()
        type = d_ptr.GetType().GetPointeeType()
        type_size = type.GetByteSize()

        i = index - self._num_data_fields
        elem = self._valobj.CreateValueFromAddress(f'[{i}]', addr + type_size * i, type)

        return elem

    def update(self):
        self._values = dict()
        self._reset_field_counter()

        d = self._valobj.GetChildMemberWithName('d')

        size = d.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE)
        self._values[self._num_data_fields] = size
        self._bump_field_counter()

        d_d = d.GetChildMemberWithName('d')

        if d_d.GetValueAsUnsigned():
            alloc = d_d.GetChildMemberWithName('alloc')
            self._values[self._num_data_fields] = self._valobj.CreateValueFromData(
                QArrayDataPointerSynth.PROP_CAPACITY, alloc.GetData(),
                alloc.GetType())
            self._bump_field_counter()

            d_ptr = d.GetChildMemberWithName('ptr')
            if d_ptr.GetValueAsUnsigned():
                self._values[self._num_data_fields] = self._valobj.CreateValueFromData(
                    QArrayDataPointerSynth.PROP_RAW_DATA, d_ptr.data,
                    d_ptr.type)
                self._bump_field_counter()

                size_v = size.GetValueAsSigned()
                alloc_v = alloc.GetValueAsSigned()
                if 0 <= size_v <= alloc_v and alloc_v >= 0:
                    # otherwise a half-initialized list
                    self._num_children += size.GetValueAsUnsigned()

        return False

    def _reset_field_counter(self):
        self._num_children = 0
        self._num_data_fields = 0

    def _bump_field_counter(self):
        self._num_data_fields += 1
        self._num_children += 1
