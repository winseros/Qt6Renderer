from helpers import DateTimeHelpers
from lldb import SBValue


def qdate_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        year = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_YEAR).GetValueAsSigned()
        month = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MONTH).GetValueAsSigned()
        day = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_DAY).GetValueAsSigned()
        return '{}-{}-{}'.format(year, zero_format(month), zero_format(day))
    else:
        return '(Invalid)'


def zero_format(n: int):
    return n if n > 9 else '0{}'.format(n)


class QDateSynth:
    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._values = []

    def has_children(self) -> bool:
        return len(self._values) > 0

    def num_children(self) -> int:
        return len(self._values)

    def get_child_index(self, name: str) -> int:
        if name == DateTimeHelpers.PROP_YEAR:
            return 0
        elif name == DateTimeHelpers.PROP_MONTH:
            return 1
        elif name == DateTimeHelpers.PROP_DAY:
            return 2
        else:
            return -1

    def get_child_at_index(self, index: int) -> SBValue:
        return self._values[index]

    def get_value(self):
        return self._valobj

    def update(self):
        jd = self._valobj.GetChildMemberWithName('jd').GetValueAsSigned()
        (year, month, day) = DateTimeHelpers.parse_julian_date(jd, self._valobj)

        if year is not None:
            self._values = [year, month, day]

        return False
