from lldb import SBValue
from .qt import qt, QtVersion
from .abstractsynth import AbstractSynth
from .qfilesystementry import QFileSystemEntry
from .qstring import qstring_summary
from .syntheticstruct import SyntheticStruct
from .qshareddatapointer import QSharedDataPointer
from .qshareddata import QSharedData


def qdir_summary(valobj):
    path = valobj.GetChildMemberWithName(QDirSynth.PROP_PATH)
    path_text = qstring_summary(path)
    return path_text


class QDirSynth(AbstractSynth):
    PROP_PATH = 'path'
    PROP_ABSOLUTE_PATH = 'absolutePath'
    PROP_EXISTS = 'exists'

    def update(self):
        # warm up caches; does not work on Windows
        self._valobj.EvaluateExpression('absolutePath()')

        if qt().version(self._valobj.target) >= QtVersion.V6_6_0:
            dir6 = QDir66(self._valobj)

            file_path = dir6.d_ptr().d().dir_entry().file_path()
            path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_PATH, file_path.load_addr, file_path.type)
            self._values = [path]

            abs_path = dir6.d_ptr().d().file_cache().absolute_dir_entry().file_path()
            absolute_path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_ABSOLUTE_PATH, abs_path.load_addr,
                                                                abs_path.type)
            self._values.append(absolute_path)
        else:
            dir6 = QDir655(self._valobj)

            file_path = dir6.d_ptr().d().path().file_path()
            path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_PATH, file_path.load_addr, file_path.type)
            self._values = [path]

            abs_path = dir6.d_ptr().d().abs_path().file_path()
            absolute_path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_ABSOLUTE_PATH, abs_path.load_addr,
                                                                abs_path.type)
            self._values.append(absolute_path)

        # the below code does not work on Windows; due to outdated LLDB, I guess
        exists = self._valobj.EvaluateExpression('exists()')
        if exists.IsValid() and exists.type.IsValid():
            exists = self._valobj.CreateValueFromAddress(QDirSynth.PROP_EXISTS, exists.load_addr, exists.type)
            self._values.append(exists)

        return False


class FileCache(SyntheticStruct):

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_named_type_field('mutex', 'QMutex')
        self.add_named_type_field('files', 'QStringList')
        self.add_named_type_field('file_infos', 'QList<int>')  # QFileInfoList
        self.add_named_type_field('file_lists_initialized', 'std::atomic<bool>')
        self.add_synthetic_field('absolute_dir_entry', lambda p: QFileSystemEntry(p))
        # self.add_named_type_field('metadata', 'QFileSystemMetadata')

    def absolute_dir_entry(self) -> QFileSystemEntry:
        pass


class QDirPrivate655(QSharedData):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_named_type_field('file_lists_initialized', 'bool')
        self.add_named_type_field('files', 'QStringList')
        self.add_named_type_field('file_infos', 'QList<int>')
        self.add_named_type_field('name_filters', 'QStringList')
        self.add_named_type_field('sort', 'QDir::SortFlags')
        self.add_named_type_field('filters', 'QDir::Filters')
        self.add_gap_field(8)  # sizeof(std::unique_ptr<>)
        self.add_synthetic_field('path', lambda p: QFileSystemEntry(p))
        self.add_synthetic_field('abs_path', lambda p: QFileSystemEntry(p))

    def path(self) -> QFileSystemEntry:
        pass

    def abs_path(self) -> QFileSystemEntry:
        pass


class QDirPrivate66(QSharedData):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)

        self.add_named_type_field('name_filters', 'QStringList')
        self.add_named_type_field('sort', 'QDir::SortFlags')
        self.add_named_type_field('filters', 'QDir::Filters')
        self.add_gap_field(8)  # sizeof(std::unique_ptr<>)
        self.add_synthetic_field('dir_entry', lambda p: QFileSystemEntry(p))
        self.add_synthetic_field('file_cache', lambda p: FileCache(p))

    def dir_entry(self) -> QFileSystemEntry:
        pass

    def file_cache(self) -> FileCache:
        pass


class QDir655(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_synthetic_field('d_ptr', lambda p: QSharedDataPointer[QDirPrivate655](p, lambda q: QDirPrivate655(q)))

    def d_ptr(self) -> QSharedDataPointer[QDirPrivate655]:
        pass


class QDir66(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_synthetic_field('d_ptr', lambda p: QSharedDataPointer[QDirPrivate66](p, lambda q: QDirPrivate66(q)))

    def d_ptr(self) -> QSharedDataPointer[QDirPrivate66]:
        pass
