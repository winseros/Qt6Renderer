from typing import Union
from lldb import SBValue, eBasicTypeInt
from .qt import qt, QtVersion
from .abstractsynth import AbstractSynth
from .qfilesystementry import QFileSystemEntry, file_system_entry_is_initialized
from .qstring import qstring_summary
from .syntheticstruct import SyntheticStruct
from .qshareddatapointer import QSharedDataPointer
from .qshareddata import QSharedData
from .platformhelpers import get_named_type, get_int_pointer_type, platform_is_windows


def qdir_summary(valobj):
    path = valobj.GetChildMemberWithName(QDirSynth.PROP_PATH)
    path_text = qstring_summary(path) if path.IsValid() else ''
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
            if not dir6.d_ptr().GetValueAsUnsigned():
                self._values = []
                return False

            dir_private = dir6.d().d()
            if not qdir_private_is_initialized(dir_private):
                return False

            file_path_entry = dir_private.dir_entry()
            absolute_dir_entry = dir_private.file_cache().absolute_dir_entry()
            if not file_system_entry_is_initialized(file_path_entry):
                return False

            if not platform_is_windows(self._valobj) and not file_system_entry_is_initialized(absolute_dir_entry):
                return False

            file_path = file_path_entry.file_path()
            path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_PATH, file_path.load_addr, file_path.type)
            self._values = [path]

            abs_path = absolute_dir_entry.file_path()
            absolute_path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_ABSOLUTE_PATH, abs_path.load_addr,
                                                                abs_path.type)
            self._values.append(absolute_path)
        else:
            dir6 = QDir655(self._valobj)
            if not dir6.d_ptr().GetValueAsUnsigned():
                self._values = []
                return False

            dir_private = dir6.d().d()
            if not qdir_private_is_initialized(dir_private):
                return False

            file_path_entry = dir_private.path()
            abs_path_entry = dir_private.abs_path()
            if not file_system_entry_is_initialized(file_path_entry):
                return False

            if not platform_is_windows(self._valobj) and not file_system_entry_is_initialized(abs_path_entry):
                return False

            file_path = file_path_entry.file_path()
            path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_PATH, file_path.load_addr, file_path.type)
            self._values = [path]

            abs_path = abs_path_entry.file_path()
            absolute_path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_ABSOLUTE_PATH, abs_path.load_addr,
                                                                abs_path.type)
            self._values.append(absolute_path)

        # the below code does not work on Windows; due to outdated LLDB, I guess
        exists = self._valobj.EvaluateExpression('exists()')
        if exists.IsValid() and exists.type.IsValid():
            exists = self._valobj.CreateValueFromData(QDirSynth.PROP_EXISTS, exists.data, exists.type)
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
        self.add_sb_type_field('sort', get_named_type(pointer.target, 'QDir::SortFlags', eBasicTypeInt))
        self.add_sb_type_field('filters', get_named_type(pointer.target, 'QDir::Filters', eBasicTypeInt))
        self.add_gap_field(8)  # sizeof(std::unique_ptr<>)
        self.add_synthetic_field('path', lambda p: QFileSystemEntry(p))
        self.add_synthetic_field('abs_path', lambda p: QFileSystemEntry(p))

    def path(self) -> QFileSystemEntry:
        pass

    def abs_path(self) -> QFileSystemEntry:
        pass

    def sort(self) -> SBValue:
        pass

    def filters(self) -> SBValue:
        pass


class QDirPrivate66(QSharedData):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)

        self.add_named_type_field('name_filters', 'QStringList')
        self.add_sb_type_field('sort', get_named_type(pointer.target, 'QDir::SortFlags', eBasicTypeInt))
        self.add_sb_type_field('filters', get_named_type(pointer.target, 'QDir::Filters', eBasicTypeInt))
        self.add_gap_field(8)  # sizeof(std::unique_ptr<>)
        self.add_synthetic_field('dir_entry', lambda p: QFileSystemEntry(p))
        self.add_synthetic_field('file_cache', lambda p: FileCache(p))

    def dir_entry(self) -> QFileSystemEntry:
        pass

    def file_cache(self) -> FileCache:
        pass

    def sort(self) -> SBValue:
        pass

    def filters(self) -> SBValue:
        pass


def qdir_private_is_initialized(qdir: Union[QDirPrivate66, QDirPrivate655]) -> bool:
    sort_no_sort = -1
    sort_type = 0x80
    sort = qdir.sort().data.sint8[0]

    if sort < sort_no_sort or sort > sort_type:
        return False

    filter_no_filter = -1
    filter_no_dot_dot = 0x4000
    fltr = qdir.filters().data.sint8[0]
    if fltr < filter_no_filter or fltr > filter_no_dot_dot:
        return False

    return True


class QDir655(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)

        self.add_synthetic_field('d', lambda p: QSharedDataPointer[QDirPrivate655](p, lambda q: QDirPrivate655(q)))
        t_ptr = get_int_pointer_type(pointer)
        self.add_gap_field(-t_ptr.size)
        self.add_sb_type_field('d_ptr', t_ptr)

    def d(self) -> QSharedDataPointer[QDirPrivate655]:
        pass

    def d_ptr(self) -> SBValue:
        pass


class QDir66(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_synthetic_field('d', lambda p: QSharedDataPointer[QDirPrivate66](p, lambda q: QDirPrivate66(q)))
        t_ptr = get_int_pointer_type(pointer)
        self.add_gap_field(-t_ptr.size)
        self.add_sb_type_field('d_ptr', t_ptr)

    def d(self) -> QSharedDataPointer[QDirPrivate66]:
        pass

    def d_ptr(self) -> SBValue:
        pass
