from lldb import SBValue
from .syntheticstruct import SyntheticStruct


class QSharedData(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_named_type_field('ref', 'QAtomicInt')
