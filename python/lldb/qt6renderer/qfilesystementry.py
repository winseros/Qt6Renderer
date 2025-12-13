from lldb import SBValue
from .syntheticstruct import SyntheticStruct
from .qarraydatapointer import QArrayDataPointerSynth


class QFileSystemEntry(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_named_type_field('file_path', 'QString')
        self.add_named_type_field('native_file_path', 'NativePath')
        self.add_named_type_field('last_separator', 'qint16')
        self.add_named_type_field('first_dot', 'qint16')
        self.add_named_type_field('last_dot', 'qint16')

    def file_path(self) -> SBValue:
        pass

    def last_separator(self) -> SBValue:
        pass

    def first_dot(self) -> SBValue:
        pass

    def last_dot(self) -> SBValue:
        pass


def file_system_entry_is_initialized(entry: QFileSystemEntry) -> bool:
    ls = entry.last_separator().GetValueAsSigned()
    if ls < -2:
        return False

    fd = entry.first_dot().GetValueAsSigned()
    if fd < -2:
        return False

    ld = entry.last_dot().GetValueAsSigned()
    if ld < -1:
        return False

    prop_size = entry.file_path().GetChildMemberWithName(QArrayDataPointerSynth.PROP_SIZE)
    if not prop_size.IsValid():
        return False

    size = prop_size.GetValueAsSigned()
    if size <= 0:
        return False

    if ls >= size or fd >= size or ld >= size:
        return False

    return True