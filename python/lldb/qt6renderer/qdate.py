from .datetimehelpers import DateTimeHelpers
from .abstractsynth import AbstractSynth


def qdate_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        year = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_YEAR).GetValueAsSigned()
        month = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MONTH).GetValueAsSigned()
        day = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_DAY).GetValueAsSigned()
        return f'{year}-{month:02d}-{day:02d}'
    else:
        return '(Invalid)'


class QDateSynth(AbstractSynth):
    def get_child_index(self, name: str) -> int:
        if name == DateTimeHelpers.PROP_YEAR:
            return 0
        elif name == DateTimeHelpers.PROP_MONTH:
            return 1
        elif name == DateTimeHelpers.PROP_DAY:
            return 2
        else:
            return -1

    def update(self):
        jd = self._valobj.GetChildMemberWithName('jd')
        (year, month, day) = DateTimeHelpers.parse_julian_date(jd.GetValueAsSigned(), jd)

        if year is not None:
            self._values = [year, month, day]

        return False
