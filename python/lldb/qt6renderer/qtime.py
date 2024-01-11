from .datetimehelpers import DateTimeHelpers
from .abstractsynth import AbstractSynth


def qtime_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        hours = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_HOURS).GetValueAsSigned()
        minutes = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MINUTES).GetValueAsSigned()
        seconds = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_SECONDS).GetValueAsSigned()
        milliseconds = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MILLISECONDS).GetValueAsSigned()
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}'
    else:
        return '(Invalid)'


class QTimeSynth(AbstractSynth):
    def get_child_index(self, name: str) -> int:
        if name == DateTimeHelpers.PROP_HOURS:
            return 0
        elif name == DateTimeHelpers.PROP_MINUTES:
            return 1
        elif name == DateTimeHelpers.PROP_SECONDS:
            return 2
        elif name == DateTimeHelpers.PROP_MILLISECONDS:
            return 3
        else:
            return -1

    def update(self):
        mds = self._valobj.GetChildMemberWithName('mds').GetValueAsSigned()

        (hours, minutes, seconds, milliseconds) = DateTimeHelpers.parse_time(mds, self._valobj)

        if hours is not None:
            self._values = [hours, minutes, seconds, milliseconds]

        return False
