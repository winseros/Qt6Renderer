from helpers import DateTimeHelpers
from lldb import SBValue


def qtime_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        hours = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_HOURS).GetValueAsSigned()
        minutes = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MINUTES).GetValueAsSigned()
        seconds = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_SECONDS).GetValueAsSigned()
        milliseconds = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MILLISECONDS).GetValueAsSigned()
        return '{}:{}:{}.{}'.format(zero_format1(hours), zero_format1(minutes), zero_format1(seconds),
                                    zero_format2(milliseconds))
    else:
        return '(Invalid)'


def zero_format1(n: int):
    return n if n > 9 else '0{}'.format(n)


def zero_format2(n: int):
    return n if n > 99 \
        else '0{}'.format(n) if n > 9 \
        else '00{}'.format(n)


class QTimeSynth:
    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._values = []

    def has_children(self) -> bool:
        return len(self._values) > 0

    def num_children(self) -> int:
        return len(self._values)

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

    def get_child_at_index(self, index: int) -> SBValue:
        return self._values[index]

    def get_value(self):
        return self._valobj

    def update(self):
        mds = self._valobj.GetChildMemberWithName('mds').GetValueAsSigned()

        (hours, minutes, seconds, milliseconds) = DateTimeHelpers.parse_time(mds, self._valobj)

        if hours is not None:
            self._values = [hours, minutes, seconds, milliseconds]

        return False
