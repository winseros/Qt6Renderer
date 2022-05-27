from lldb import SBValue
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

    def get_child_index(self, name: str) -> int:
        if name == QFileSynth.PROP_FILE_NAME:
            return 0
        else:
            return -1

    def update(self):
        offset = 424

        addr = self._valobj.load_addr
        print(111)
        print(addr)
        print(hex(addr))
        type_qstring = self._valobj.GetFrame().GetModule().FindFirstType('QString')
        print(222)
        print(addr)
        print(hex(addr))
        fileName = self._valobj.CreateValueFromAddress(QFileSynth.PROP_FILE_NAME, addr + offset,
                                                       type_qstring)

        print(fileName)

        # does not work on windows with MSVC compiler
        exists = QtHelpers.evaluate_bool(self._valobj, 'exists')

        self._values = [fileName, exists]

        return False

    def _evaluate_bool(self, getter: str) -> SBValue:
        target = self._valobj.GetTarget()
        var_name = self._valobj.GetName()

        val = target.EvaluateExpression(f'{var_name}.{getter}()')
        named_val = self._valobj.CreateValueFromData(getter, val.GetData(), val.GetType())
        return named_val
