from qstring import qstring_summary
from lldb import eBasicTypeBool
from abstractsynth import AbstractSynth


def qtemporarydir_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        path = valobj.GetChildMemberWithName(QTemporaryDirSynth.PROP_PATH_OR_ERROR)
        path_text = qstring_summary(path)
        return path_text
    else:
        return '(Null)'

class QTemporaryDirSynth(AbstractSynth):
    PROP_PATH_OR_ERROR = 'pathOrError'
    PROP_AUTO_REMOVE = 'autoRemove'
    PROP_SUCCESS = 'success'

    def get_child_index(self, name: str) -> int:
        if name == QTemporaryDirSynth.PROP_PATH_OR_ERROR:
            return 0
        elif name == QTemporaryDirSynth.PROP_AUTO_REMOVE:
            return 1
        elif name == QTemporaryDirSynth.PROP_SUCCESS:
            return 2
        else:
            return -1

    def update(self):
        type_qstring = self._valobj.GetFrame().GetModule().FindFirstType('QString')
        type_bool = self._valobj.GetTarget().GetBasicType(eBasicTypeBool)

        addr = self._valobj.GetChildMemberWithName('d_ptr').GetChildMemberWithName('d').GetValueAsUnsigned()
        path_or_error = self._valobj.CreateValueFromAddress(QTemporaryDirSynth.PROP_PATH_OR_ERROR, addr, type_qstring)
        auto_remove = self._valobj.CreateValueFromAddress(QTemporaryDirSynth.PROP_AUTO_REMOVE, addr + type_qstring.size, type_bool)
        success = self._valobj.CreateValueFromAddress(QTemporaryDirSynth.PROP_SUCCESS, addr + type_qstring.size + 1, type_bool)

        self._values = [path_or_error, auto_remove, success]

        return False

