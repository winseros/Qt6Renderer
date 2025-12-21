from lldb import SBValue
from .abstractsynth import AbstractSynth
from .qshareddata import QSharedData
from .qfilesystementry import QFileSystemEntry, file_system_entry_is_initialized
from .qstring import qstring_summary
from .syntheticstruct import SyntheticStruct
from .qshareddatapointer import QSharedDataPointer
from .platformhelpers import get_int_pointer_type


def qfileinfo_summary(valobj: SBValue) -> str:
    prop = valobj.GetChildMemberWithName(QFileInfoSynth.PROP_PATH)
    text = qstring_summary(prop) if prop.IsValid() else '""'
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

    def update(self) -> bool:
        fi = QFileInfo(self._valobj)
        if not fi.d_ptr().GetValueAsUnsigned():
            self._values = []
            return False

        file_entry = fi.d().d().file_entry()
        if not file_system_entry_is_initialized(file_entry):
            return False

        file_path = file_entry.file_path()
        self._values = [self._valobj.CreateValueFromAddress(QFileInfoSynth.PROP_PATH, file_path.load_addr, file_path.type)]

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
        self.add_synthetic_field('file_entry', lambda p: QFileSystemEntry(p))

    def file_entry(self) -> QFileSystemEntry:
        pass


class QFileInfo(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_synthetic_field('d', lambda p: QSharedDataPointer(p, lambda q: QFileInfoPrivate(q)))
        t_ptr = get_int_pointer_type(pointer)
        self.add_gap_field(-t_ptr.size)
        self.add_sb_type_field('d_ptr', t_ptr)

    def d(self) -> QSharedDataPointer[QFileInfoPrivate]:
        pass

    def d_ptr(self) -> SBValue:
        pass
