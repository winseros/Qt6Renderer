from lldb import SBValue, SBData, eBasicTypeLongLong, eBasicTypeInt
from .lazysynth import LazySynth
from .syntheticstruct import SyntheticStruct
from typing import Callable, Generic, TypeVar, Union
from .platformhelpers import get_void_pointer_type, get_named_type


class QArrayData(SyntheticStruct):
    FLAG_ARRAY_OPTION_DEFAULT = 0x0
    FLAG_ARRAY_OPTION_RESERVED = 0x1

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)

        self.add_named_type_field('ref', 'QBasicAtomicInt')
        self.add_sb_type_field('flags', get_named_type(pointer.target, 'QArrayData::ArrayOption', eBasicTypeInt))
        self.add_basic_type_field('alloc', eBasicTypeLongLong)

    def alloc(self) -> SBValue:
        pass


T = TypeVar('T')


class QArrayDataPointer(SyntheticStruct, Generic[T]):
    def __init__(self, pointer: SBValue, element_ctor: Callable[[SBValue], SyntheticStruct]):
        super().__init__(pointer)

        self._element_ctor = element_ctor
        self._element_size_value = None
        self._element_type = pointer.target.GetBasicType(eBasicTypeInt)
        self.add_synthetic_field_pointer('get_d', lambda p: QArrayData(p))
        self.add_sb_type_field('get_ptr', get_void_pointer_type(pointer))
        self.add_basic_type_field('get_size', eBasicTypeLongLong)

    def get_d(self) -> QArrayData:
        pass

    def get_ptr(self) -> SBValue:
        pass

    def get_size(self) -> SBValue:
        # just "size" conflicts with the SyntheticStruct property
        pass

    def element_at(self, index: int, value_name: Callable[[int], str] = None) -> Union[T, None]:
        if not self.get_ptr():
            return None

        name = value_name(index) if value_name else f'[{index}]'

        element_addr = self.get_ptr().GetValueAsUnsigned() + self._element_size * index
        element_ref = self._pointer.CreateValueFromAddress(name, element_addr, self._element_type)

        element = self._element_ctor(element_ref)
        return element

    @property
    def _element_size(self):
        if not self._element_size_value:
            element = self._element_ctor(self._pointer)
            self._element_size_value = element.size
        return self._element_size_value


class QArrayDataPointerContainer(Generic[T], SyntheticStruct):
    def __init__(self, valobj: SBValue, element_ctor: Callable[[SBValue], T]):
        super().__init__(valobj)
        self.add_synthetic_field('d', lambda p: QArrayDataPointer(p, element_ctor))

    def d(self) -> QArrayDataPointer[T]:
        pass


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
        elif self._num_data_fields > 1 and name == self.PROP_CAPACITY:
            return 1
        elif self._num_data_fields > 2 and name == self.PROP_RAW_DATA:
            return 2
        elif self._num_data_fields > 3:
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
        self._add_field(size)

        d_d = d.GetChildMemberWithName('d')

        if d_d.GetValueAsUnsigned():
            flags = d_d.GetChildMemberWithName('flags').data.sint8[0]
            if flags != QArrayData.FLAG_ARRAY_OPTION_DEFAULT and flags != QArrayData.FLAG_ARRAY_OPTION_RESERVED:
                # a half-initialized list
                return False

            alloc = d_d.GetChildMemberWithName('alloc')

            size_v = size.GetValueAsSigned()
            alloc_v = alloc.GetValueAsSigned()

            if size_v > alloc_v:
                # a half-initialized list
                return False

            alloc = self._valobj.CreateValueFromData(
                QArrayDataPointerSynth.PROP_CAPACITY, alloc.GetData() if alloc else SBData.CreateDataFromInt(0),
                alloc.GetType() if alloc else self._valobj.target.GetBasicType(eBasicTypeInt))
            self._add_field(alloc)

            if size_v <= 0 or alloc_v <= 0:
                return False

            d_ptr = d.GetChildMemberWithName('ptr')
            if d_ptr.GetValueAsUnsigned():
                d_ptr = self._valobj.CreateValueFromAddress(
                    QArrayDataPointerSynth.PROP_RAW_DATA, d_ptr.load_addr, d_ptr.type)
                self._add_field(d_ptr)
                self._num_children += size.GetValueAsUnsigned()

        return False

    def _add_field(self, field: SBValue) -> None:
        self._values[self._num_data_fields] = field
        self._bump_field_counter()

    def _reset_field_counter(self):
        self._num_children = 0
        self._num_data_fields = 0

    def _bump_field_counter(self):
        self._num_data_fields += 1
        self._num_children += 1
