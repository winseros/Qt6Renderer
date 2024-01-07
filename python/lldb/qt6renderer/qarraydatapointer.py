from .abstractsynth import AbstractSynth


class QArrayDataPointerSynth(AbstractSynth):
    # the provider layout is:
    # [size]
    # [capacity]
    # [0..n]

    # the constant marks the range of properties, where [0..n] is
    RANGE_START_OFFSET = 2

    PROP_SIZE = 'size'
    PROP_CAPACITY = 'capacity'

    def get_child_index(self, name: str) -> int:
        if name == self.PROP_SIZE:
            return 0
        elif name == self.PROP_CAPACITY:
            return 1
        else:
            index = name.lstrip('[').rstrip(']')
            if index.isdigit():
                return int(index) + self.RANGE_START_OFFSET
            else:
                return -1

    def update(self):
        d = self._valobj.GetChildMemberWithName('d')
        size = d.GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE)
        self._values.append(size)

        d_ptr = d.GetChildMemberWithName('ptr')
        if d_ptr.GetValueAsUnsigned():
            alloc = d.GetChildMemberWithName('d').GetChildMemberWithName('alloc')
            self._values.append(self._valobj.CreateValueFromData(QArrayDataPointerSynth.PROP_CAPACITY, alloc.GetData(),
                                                                 alloc.GetType()))

            addr = d_ptr.GetValueAsUnsigned()
            type = d_ptr.GetType().GetPointeeType()
            type_size = type.GetByteSize()
            for i in range(0, size.GetValueAsSigned()):
                elem = self._valobj.CreateValueFromAddress(f'[{i}]', addr + type_size * i, type)
                self._values.append(elem)

        return False
