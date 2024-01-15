from lldb import SBValue, eBasicTypeBool

from .abstractsynth import AbstractSynth
from .syntheticstruct import SyntheticStruct
from .qstring import qstring_summary
from .qt import qt, QtVersion


def qtemporarydir_summary(valobj: SBValue) -> str:
    prop = valobj.GetChildMemberWithName(QTemporaryDirPrivate.PROP_PATH_OR_ERROR)
    text = qstring_summary(prop)
    return text


class QTemporaryDirSynth(AbstractSynth):
    def get_child_index(self, name: str) -> int:
        if name == QTemporaryDirPrivate.PROP_PATH_OR_ERROR:
            return 0
        elif name == QTemporaryDirPrivate.PROP_AUTO_REMOVE:
            return 1
        elif name == QTemporaryDirPrivate.PROP_SUCCESS:
            return 2
        else:
            return -1

    def update(self) -> bool:
        if qt().version(self._valobj.target) >= QtVersion.V6_4_0:
            d = self._valobj.GetChildMemberWithName('d_ptr')  # QDirPrivate* since 6.4.0
        else:
            d = self._valobj.GetChildMemberWithName('d_ptr').GetChildMemberWithName('d')  # QSharedDataPointer

        private = QTemporaryDirPrivate(d)

        self._values = [private.path_or_error(), private.auto_remove(), private.success()]

        return False


class QTemporaryDirPrivate(SyntheticStruct):
    PROP_PATH_OR_ERROR = 'pathOrError'
    PROP_AUTO_REMOVE = 'autoRemove'
    PROP_SUCCESS = 'success'

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_named_type_field(QTemporaryDirPrivate.PROP_PATH_OR_ERROR, 'QString', 'path_or_error')
        self.add_basic_type_field(QTemporaryDirPrivate.PROP_AUTO_REMOVE, eBasicTypeBool, getter_name='auto_remove')
        self.add_basic_type_field(QTemporaryDirPrivate.PROP_SUCCESS, eBasicTypeBool)

    def path_or_error(self) -> SBValue:
        pass

    def auto_remove(self) -> SBValue:
        pass

    def success(self) -> SBValue:
        pass
