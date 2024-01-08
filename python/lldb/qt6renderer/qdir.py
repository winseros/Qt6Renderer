from .qt import qt, QtVersion
from .qstring import qstring_summary
from .abstractsynth import AbstractSynth
from .platformhelpers import platform_is_32bit


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
        bit32 = platform_is_32bit(self._valobj)

        if qt().version() >= QtVersion.V6_6_0:
            if bit32:
                dirEntryOffset = 24
                fileCacheOffset = 52
                absoluteDirEntryOffset = fileCacheOffset + 32
            else:
                dirEntryOffset = 48
                fileCacheOffset = 104
                absoluteDirEntryOffset = fileCacheOffset + 64
        else:
            if bit32:
                dirEntryOffset = 40
                absoluteDirEntryOffset = 72
            else:
                dirEntryOffset = 96
                absoluteDirEntryOffset = 152

        type_qstring = self._valobj.target.FindFirstType('QString')
        addr = self._valobj.GetChildMemberWithName('d_ptr').GetChildMemberWithName('d').GetValueAsUnsigned()

        path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_PATH, addr + dirEntryOffset, type_qstring)
        self._values = [path]

        # warm up caches; does not work on Windows
        self._valobj.EvaluateExpression('absolutePath()')

        absolute_path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_ABSOLUTE_PATH, addr + absoluteDirEntryOffset,
                                                            type_qstring)
        self._values.append(absolute_path)

        # the below code does not work on Windows; due to outdated LLDB, I guess
        exists = self._valobj.EvaluateExpression('exists()')
        if exists.IsValid() and exists.type.IsValid():
            exists = self._valobj.CreateValueFromData(QDirSynth.PROP_EXISTS, exists.data, exists.type)
            self._values.append(exists)

        return False
