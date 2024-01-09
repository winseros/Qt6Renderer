from lldb import SBValue, eBasicTypeBool
from .abstractsynth import AbstractSynth
from .qshareddata import QSharedData
from .qfilesystementry import QFileSystemEntry
from .qstring import qstring_summary


def qfileinfo_summary(valobj: SBValue) -> str:
    prop = valobj.GetChildMemberWithName(QFileInfoSynth.PROP_PATH)
    text = qstring_summary(prop)
    return text


class QFileInfoSynth(AbstractSynth):
    PROP_PATH = 'path'
    PROP_CACHING = 'caching'
    PROP_EXISTS = 'exists'
    PROP_IS_DIR = 'isDir'
    PROP_IS_EXECUTABLE = 'isExecutable'
    PROP_IS_FILE = 'isFile'
    PROP_IS_HIDDEN = 'isHidden'
    PROP_IS_READABLE = 'isReadable'
    PROP_IS_RELATIVE = 'isRelative'
    PROP_IS_SYMLINK = 'isSymLink'
    PROP_IS_WRITABLE = 'isWritable'

    def get_child_index(self, name: str) -> int:
        if name == QFileInfoSynth.PROP_PATH:
            return 0
        elif name == QFileInfoSynth.PROP_CACHING and self.num_children() > 1:
            return 1
        elif name == QFileInfoSynth.PROP_EXISTS and self.num_children() > 2:
            return 2
        elif name == QFileInfoSynth.PROP_IS_DIR and self.num_children() > 3:
            return 3
        elif name == QFileInfoSynth.PROP_IS_EXECUTABLE and self.num_children() > 4:
            return 4
        elif name == QFileInfoSynth.PROP_IS_FILE and self.num_children() > 5:
            return 5
        elif name == QFileInfoSynth.PROP_IS_HIDDEN and self.num_children() > 6:
            return 6
        elif name == QFileInfoSynth.PROP_IS_READABLE and self.num_children() > 7:
            return 7
        elif name == QFileInfoSynth.PROP_IS_RELATIVE and self.num_children() > 8:
            return 8
        elif name == QFileInfoSynth.PROP_IS_SYMLINK and self.num_children() > 9:
            return 9
        elif name == QFileInfoSynth.PROP_IS_WRITABLE and self.num_children() > 10:
            return 10
        else:
            return -1

    def update(self) -> bool:
        d = self._valobj.GetChildMemberWithName('d_ptr').GetChildMemberWithName('d')
        private = QFileInfoPrivate(d)

        file_path = private.file_entry().file_path()
        self._values = [self._valobj.CreateValueFromData(QFileInfoSynth.PROP_PATH, file_path.data, file_path.type)]

        [self._try_add_property(x) for x in [QFileInfoSynth.PROP_CACHING, QFileInfoSynth.PROP_EXISTS,
                                             QFileInfoSynth.PROP_IS_DIR, QFileInfoSynth.PROP_IS_EXECUTABLE,
                                             QFileInfoSynth.PROP_IS_FILE, QFileInfoSynth.PROP_IS_HIDDEN,
                                             QFileInfoSynth.PROP_IS_READABLE, QFileInfoSynth.PROP_IS_RELATIVE,
                                             QFileInfoSynth.PROP_IS_SYMLINK, QFileInfoSynth.PROP_IS_WRITABLE]]

        return False

    def _try_add_property(self, prop_name: str):
        val = self._valobj.EvaluateExpression(f'{prop_name}()')
        if val.IsValid() and val.type.IsValid():
            self._values.append(self._valobj.CreateValueFromData(prop_name, val.data, val.type))


class QFileInfoPrivate(QSharedData):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_synthetic_field('file_entry', QFileSystemEntry(pointer))

    def file_entry(self) -> QFileSystemEntry:
        pass
