from qstring import qstring_summary
from helpers import QtHelpers
from abstractsynth import AbstractSynth


def qdir_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        path = valobj.GetChildMemberWithName(QDirSynth.PROP_ABSOLUTE_PATH)
        path_text = qstring_summary(path)
        return path_text
    else:
        return '(Null)'

class QDirSynth(AbstractSynth):
    PROP_PATH = 'path'
    PROP_ABSOLUTE_PATH = 'absolutePath'

    def get_child_index(self, name: str) -> int:
        if name == QDirSynth.PROP_PATH:
            return 0
        elif name == QDirSynth.PROP_ABSOLUTE_PATH:
            return 1
        else:
            return -1

    def update(self):
        type_qstring = self._valobj.GetFrame().GetModule().FindFirstType('QString')

        addr = self._valobj.GetChildMemberWithName('d_ptr').GetChildMemberWithName('d').GetValueAsUnsigned()

        dirEntryOffset = 96
        absoluteDirEntryOffset = 152

        # warm up internal caches
        # TODO: works on Linux, check on Windows
        self._valobj.GetTarget().EvaluateExpression(f'{self._valobj.name}.absolutePath')

        path = self._valobj.CreateValueFromAddress(QDirSynth.PROP_PATH, addr + dirEntryOffset, type_qstring)
        absolutePath = self._valobj.CreateValueFromAddress(QDirSynth.PROP_ABSOLUTE_PATH, addr + absoluteDirEntryOffset, type_qstring)

        # does not work on Windows with MSVC compiler
        exists = QtHelpers.evaluate_bool(self._valobj, 'exists')

        self._values = [path, absolutePath, exists]

        return False

