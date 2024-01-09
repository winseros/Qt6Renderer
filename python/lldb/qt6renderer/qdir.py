from lldb import SBValue
from .qt import qt, QtVersion
from .abstractsynth import AbstractSynth
from .qfilesystementry import QFileSystemEntry
from .qstring import qstring_summary
from .platformhelpers import platform_is_32bit
from .syntheticstruct import SyntheticStruct


def qdir_summary(valobj):
    path = valobj.GetChildMemberWithName(QDirSynth.PROP_PATH)
    path_text = qstring_summary(path)
    return path_text


class QDirSynth(AbstractSynth):
    PROP_PATH = 'path'
    PROP_ABSOLUTE_PATH = 'absolutePath'
    PROP_EXISTS = 'exists'

    def get_child_index(self, name: str) -> int:
        num_children = self.num_children()
        if name == QDirSynth.PROP_PATH:
            return 0
        elif name == QDirSynth.PROP_ABSOLUTE_PATH:
            return 1
        elif num_children > 1 and name == QDirSynth.PROP_EXISTS:
            return 2
        else:
            return -1

    def update(self):
        priv = QDirPrivate(self._valobj.GetChildMemberWithName('d_ptr').GetChildMemberWithName('d'))

        path = self._valobj.CreateValueFromData(QDirSynth.PROP_PATH, priv.path().file_path().data,
                                                priv.path().file_path().type)
        self._values = [path]

        # warm up caches; does not work on Windows
        self._valobj.EvaluateExpression('absolutePath()')

        absolute_path = self._valobj.CreateValueFromData(QDirSynth.PROP_ABSOLUTE_PATH,
                                                         priv.abs_path().file_path().data,
                                                         priv.abs_path().file_path().type)
        self._values.append(absolute_path)

        # the below code does not work on Windows; due to outdated LLDB, I guess
        exists = self._valobj.EvaluateExpression('exists()')
        if exists.IsValid() and exists.type.IsValid():
            exists = self._valobj.CreateValueFromData(QDirSynth.PROP_EXISTS, exists.data, exists.type)
            self._values.append(exists)

        return False


class QDirPrivate(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_gap_field(self._get_offset())
        self.add_synthetic_field('path', QFileSystemEntry(pointer))
        self.add_synthetic_field('abs_path', QFileSystemEntry(pointer))

    def path(self) -> QFileSystemEntry:
        pass

    def abs_path(self) -> QFileSystemEntry:
        pass

    def _get_offset(self):
        bit32 = platform_is_32bit(self._pointer)

        if qt().version() >= QtVersion.V6_6_0:
            if bit32:
                offset = 24
            else:
                offset = 48
        else:
            if bit32:
                offset = 40
            else:
                offset = 96

        return offset
