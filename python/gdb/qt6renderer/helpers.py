from gdb import Value
from typing import Tuple


def has_cpp_type(valobj: Value, cpp_name: str) -> bool:
    type_tag = _get_type_tag(valobj)
    if not type_tag:
        return False
    result = type_tag == cpp_name
    return result


def has_cpp_generic_type(valobj: Value, cpp_name: str, suffix: str = None) -> bool:
    type_tag = _get_type_tag(valobj)
    if not type_tag:
        return False
    result = type_tag.startswith(cpp_name + '<') and type_tag.endswith(f'>{suffix}')
    return result


def _get_type_tag(valobj: Value) -> str:
    type = valobj.type
    tag = type.tag if type.tag else type.strip_typedefs().tag
    return tag


class DateTimeHelpers:
    PROP_YEAR = 'year'
    PROP_MONTH = 'month'
    PROP_DAY = 'day'
    PROP_HOURS = 'hours'
    PROP_MINUTES = 'minutes'
    PROP_SECONDS = 'seconds'
    PROP_MILLISECONDS = 'milliseconds'
    PROP_INVALID = 'invalid'
    VAL_INVALID = '(Invalid)'

    _JD_MIN = -784350574879
    _JD_MAX = 784354017364
    _JD_EPOCH = 2440588  # 1970-01-01T00:00:00Z

    _MSEC_PER_SEC = 1000
    _SEC_PER_MIN = 60
    _MIN_PER_HOUR = 60
    _MSEC_PER_DAY = 86_400_000

    @staticmethod
    def parse_julian_date(jd: int) -> Tuple[int, int, int]:
        if jd < DateTimeHelpers._JD_MIN or jd > DateTimeHelpers._JD_MAX:
            return 0, 0, 0

        # The below code is from the Qt sources:

        # Math from The Calendar FAQ at http://www.tondering.dk/claus/cal/julperiod.php
        # This formula is correct for all julian days, when using mathematical integer
        # division (round to negative infinity), not c++11 integer division (round to zero)

        a = jd + 32044
        b = divmod(4 * a + 3, 146097)[0]
        c = a - divmod(146097 * b, 4)[0]

        d = divmod(4 * c + 3, 1461)[0]
        e = c - divmod(1461 * d, 4)[0]
        m = divmod(5 * e + 2, 153)[0]

        y = 100 * b + d - 4800 + divmod(m, 10)[0]

        # Adjust for no year 0
        year = int(y if y > 0 else y - 1)
        month = int(m + 3 - 12 * divmod(m, 10)[0])
        day = int(e - divmod(153 * m + 2, 5)[0] + 1)

        return year, month, day

    @staticmethod
    def parse_time(mds: int) -> Tuple[int, int, int, int]:
        if mds == -1:
            return 0, 0, 0, 0

        (mds, milliseconds) = divmod(mds, DateTimeHelpers._MSEC_PER_SEC)
        (mds, seconds) = divmod(mds, DateTimeHelpers._SEC_PER_MIN)
        (hours, minutes) = divmod(mds, DateTimeHelpers._MIN_PER_HOUR)

        return hours, minutes, seconds, milliseconds

    @staticmethod
    def msecs_to_date_time(msecs: int) -> Tuple[int, int]:
        jd = DateTimeHelpers._JD_EPOCH

        if msecs >= DateTimeHelpers._MSEC_PER_DAY or msecs <= -DateTimeHelpers._MSEC_PER_DAY:
            jd += msecs / DateTimeHelpers._MSEC_PER_DAY
            msecs %= DateTimeHelpers._MSEC_PER_DAY

        if msecs < 0:
            ds = DateTimeHelpers._MSEC_PER_DAY - msecs - 1
            jd -= ds / DateTimeHelpers._MSEC_PER_DAY
            ds = ds % DateTimeHelpers._MSEC_PER_DAY
            ds = DateTimeHelpers._MSEC_PER_DAY - ds - 1
        else:
            ds = msecs

        return jd, ds
