from lldb import SBValue, eBasicTypeBool
from qstring import qstring_summary
from helpers import QtHelpers
from abstractsynth import AbstractSynth


def qfile_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        path = valobj.GetChildMemberWithName(QFileSynth.PROP_FILE_NAME)
        path_text = qstring_summary(path)
        return path_text
    else:
        return '(Null)'


class QFileSynth(AbstractSynth):
    PROP_FILE_NAME = 'fileName'
    PROP_EXISTS = 'exists'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._type_qstring = valobj.GetFrame().GetModule().FindFirstType('QString')

    def has_children(self) -> bool:
        return True

    def get_child_index(self, name: str) -> int:
        if name == QFileSynth.PROP_FILE_NAME:
            return 0
        elif name == QFileSynth.PROP_EXISTS and len(self._values) > 1 and self._values[1].name == self.PROP_EXISTS:
            return 1
        else:
            return -1

    def update(self):
        d = self._valobj.GetChildAtIndex(0) \
            .GetChildAtIndex(0) \
            .GetChildAtIndex(0) \
            .GetChildMemberWithName('d_ptr') \
            .GetChildMemberWithName('d') \
            .GetValueAsUnsigned()

        offset = 304
        file_name = self._valobj.CreateValueFromAddress(self.PROP_FILE_NAME, d + offset, self._type_qstring)
        self._values = [file_name]

        exists = QtHelpers.evaluate_bool(self._valobj, self.PROP_EXISTS)
        if exists.type.IsValid():
            # MSVC won`t pass here
            self._values.append(exists)

        return False


class QTemporaryFileSynth(QFileSynth):
    PROP_AUTO_REMOVE = 'autoRemove'
    PROP_TEMPLATE_NAME = 'templateName'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj.GetChildAtIndex(0))
        self._type_bool = valobj.GetTarget().GetBasicType(eBasicTypeBool)

    def get_child_index(self, name: str) -> int:
        index = super(QTemporaryFileSynth, self).get_child_index(name)
        if index >= 0:
            return index
        else:
            if name == self.PROP_AUTO_REMOVE:
                return len(self._values) - 2
            elif name == self.PROP_TEMPLATE_NAME:
                return len(self._values) - 1
            else:
                return -1

    def update(self):
        super().update()

        d = self._valobj.GetChildAtIndex(0) \
            .GetChildAtIndex(0) \
            .GetChildAtIndex(0) \
            .GetChildMemberWithName('d_ptr') \
            .GetChildMemberWithName('d') \
            .GetValueAsUnsigned()

        offset = 328
        auto_remove = self._valobj.CreateValueFromAddress(self.PROP_AUTO_REMOVE, d + offset, self._type_bool)
        template_name = self._valobj.CreateValueFromAddress(self.PROP_TEMPLATE_NAME, d + offset + 8, self._type_qstring)

        self._values.append(auto_remove)
        self._values.append(template_name)
        
        return False
