from qstring import qstring_summary
from helpers import QtHelpers
from abstractsynth import AbstractSynth


def qfileinfo_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        path = valobj.GetChildMemberWithName(QFileInfoSynth.PROP_ABSOLUTE_FILE_PATH)
        path_text = qstring_summary(path)
        return path_text
    else:
        return '(Null)'

class QFileInfoSynth(AbstractSynth):
    PROP_ABSOLUTE_FILE_PATH = 'absoluteFilePath'

    def get_child_index(self, name: str) -> int:
        if name == QFileInfoSynth.PROP_ABSOLUTE_FILE_PATH:
            return 0
        else:
            return -1

    def update(self):
        ptr_size = self._valobj.GetProcess().GetAddressByteSize()
        type_qstring = self._valobj.GetFrame().GetModule().FindFirstType('QString')

        addr = self._valobj.GetChildMemberWithName('d_ptr').GetChildMemberWithName('d').GetValueAsUnsigned()

        absoluteFilePath = self._valobj.CreateValueFromAddress(QFileInfoSynth.PROP_ABSOLUTE_FILE_PATH, addr + ptr_size, type_qstring)

        # does not work on windows with MSVC compiler
        caching = QtHelpers.evaluate_bool(self._valobj, 'caching')
        exists = QtHelpers.evaluate_bool(self._valobj, 'exists')
        is_dir = QtHelpers.evaluate_bool(self._valobj, 'isDir')
        is_executable = QtHelpers.evaluate_bool(self._valobj, 'isExecutable')
        is_file = QtHelpers.evaluate_bool(self._valobj, 'isFile')
        is_hidden = QtHelpers.evaluate_bool(self._valobj, 'isHidden')
        is_readable = QtHelpers.evaluate_bool(self._valobj, 'isReadable')
        is_relative = QtHelpers.evaluate_bool(self._valobj, 'isRelative')
        is_symlink = QtHelpers.evaluate_bool(self._valobj, 'isSymLink')
        is_writable = QtHelpers.evaluate_bool(self._valobj, 'isWritable')

        self._values = [absoluteFilePath,
                        caching,
                        exists,
                        is_dir,
                        is_executable,
                        is_file,
                        is_hidden,
                        is_readable,
                        is_relative,
                        is_symlink,
                        is_writable]

        return False

