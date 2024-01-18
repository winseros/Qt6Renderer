from lldb import SBValue
from .syntheticstruct import SyntheticStruct


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
