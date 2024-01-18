from lldb import SBValue, eBasicTypeBool
from .qstring import qstring_summary
from .abstractsynth import AbstractSynth
from .qt import qt, QtVersion
from .platformhelpers import platform_is_32bit, platform_is_windows
from .syntheticstruct import SyntheticStruct
from .qshareddatapointer import QSharedDataPointer


def qfile_summary(valobj):
    path = valobj.GetChildMemberWithName(QFilePrivate.PROP_FILE_NAME)
    path_text = qstring_summary(path)
    return path_text


class QFileSynth(AbstractSynth):
    PROP_EXISTS = 'exists'

    def get_child_index(self, name: str) -> int:
        if name == QFilePrivate.PROP_FILE_NAME:
            return 0
        elif name == QFileSynth.PROP_EXISTS and self.num_children() > 1:
            return 1
        else:
            return -1

    def update(self):
        file = self._get_internal()
        self._values = [file.d_ptr().d().file_name()]

        # the below code does not work on Windows; due to outdated LLDB, I guess
        exists = self._valobj.EvaluateExpression('exists()')
        if exists.IsValid() and exists.type.IsValid():
            exists = self._valobj.CreateValueFromData(QFileSynth.PROP_EXISTS, exists.data, exists.type)
            self._values.append(exists)

        return False

    def _get_internal(self):
        return QFile(self._valobj)


class QFilePrivate(SyntheticStruct):
    PROP_FILE_NAME = 'fileName'

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_gap_field(self._get_struct_offset(pointer))
        self.add_named_type_field(QFilePrivate.PROP_FILE_NAME, 'QString', 'file_name')

    def file_name(self) -> SBValue:
        pass

    @staticmethod
    def _get_struct_offset(pointer: SBValue):
        is32bit = platform_is_32bit(pointer)
        windows = platform_is_windows(pointer)

        if qt().version(pointer.target) >= QtVersion.V6_3_0:
            if windows:
                offset = 0 if is32bit else 424
            else:
                offset = 300 if is32bit else 424
        else:
            if windows:
                offset = 0 if is32bit else 304
            else:
                offset = 196 if is32bit else 304

        return offset


class QFile(SyntheticStruct):

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_gap_field(pointer.target.GetAddressByteSize())
        self.add_synthetic_field('d_ptr', lambda p: QSharedDataPointer(p, lambda q: QFilePrivate(q)))

    def d_ptr(self) -> QSharedDataPointer[QFilePrivate]:
        pass


class QTemporaryFileSynth(QFileSynth):
    def get_child_index(self, name: str) -> int:
        index = super().get_child_index(name)
        if index >= 0:
            return index
        else:
            if name == QTemporaryFilePrivate.PROP_AUTO_REMOVE:
                return self.num_children() - 2
            elif name == QTemporaryFilePrivate.PROP_TEMPLATE_NAME:
                return self.num_children() - 1
            else:
                return -1

    def update(self):
        super().update()

        tf = self._get_internal()

        self._values.append(tf.d_ptr().d().auto_remove())
        self._values.append(tf.d_ptr().d().template_name())

        return False

    def _get_internal(self):
        return QTemporaryFile(self._valobj)


class QTemporaryFilePrivate(QFilePrivate):
    PROP_AUTO_REMOVE = 'autoRemove'
    PROP_TEMPLATE_NAME = 'templateName'

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_basic_type_field(QTemporaryFilePrivate.PROP_AUTO_REMOVE, eBasicTypeBool,
                                  getter_name='auto_remove')
        self.add_named_type_field(QTemporaryFilePrivate.PROP_TEMPLATE_NAME, 'QString', 'template_name')

    def auto_remove(self) -> SBValue:
        pass

    def template_name(self) -> SBValue:
        pass


class QTemporaryFile(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_gap_field(pointer.target.GetAddressByteSize())
        self.add_synthetic_field('d_ptr', lambda p: QSharedDataPointer(p, lambda q: QTemporaryFilePrivate(q)))

    def d_ptr(self) -> QSharedDataPointer[QTemporaryFilePrivate]:
        pass
