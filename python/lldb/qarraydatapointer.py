from abstractsynth import AbstractSynth


class QArrayDataPointerSynth(AbstractSynth):
    # the provider layout is:
    # [size]
    # [capacity]
    # [raw_data]
    # [0..n]
    RANGE_START_OFFSET = 3
    # the above constant mark the range of properties, where [0..n] is

    PROP_SIZE = 'size'
    PROP_CAPACITY = 'capacity'
    PROP_RAW_DATA = 'raw_data'

    def get_child_index(self, name: str) -> int:
        if name == self.PROP_SIZE:
            return 0
        elif name == self.PROP_CAPACITY:
            return 1
        elif name == self.PROP_RAW_DATA:
            return 2
        else:
            index = name.lstrip('[').rstrip(']')
            if index.isdigit():
                return int(index) + self.RANGE_START_OFFSET
            else:
                return -1

    def update(self):
        d = self._valobj.GetChildMemberWithName('d')
        d_size = d.GetChildMemberWithName('size')
        d_size_val = d_size.GetValueAsUnsigned()

        d_ptr = d.GetChildMemberWithName('ptr')
        d_ptr_type = d_ptr.GetType().GetPointeeType()
        d_ptr_val = d_ptr.GetValueAsUnsigned()

        d_d = d.GetChildMemberWithName('d')
        d_d_alloc = d_d.GetChildMemberWithName('alloc')

        self._values = [
            self._valobj.CreateValueFromData(self.PROP_SIZE, d_size.GetData(), d_size.GetType()),
            self._valobj.CreateValueFromData(self.PROP_CAPACITY, d_d_alloc.GetData(),
                                             d_d_alloc.GetType()),
            self._valobj.CreateValueFromData(self.PROP_RAW_DATA, d.GetData(), d.GetType())
        ]

        for i in range(d_size_val):
            self._values.append(self._valobj.CreateValueFromAddress(f'[{i}]', d_ptr_val + i * d_ptr_type.size,
                                                                    d_ptr_type))

        return False
