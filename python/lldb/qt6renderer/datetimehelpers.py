from lldb import SBValue, SBData, eBasicTypeInt

import math


class DateTimeHelpers:
    PROP_YEAR = 'year'
    PROP_MONTH = 'month'
    PROP_DAY = 'day'
    PROP_HOURS = 'hours'
    PROP_MINUTES = 'minutes'
    PROP_SECONDS = 'seconds'
    PROP_MILLISECONDS = 'milliseconds'

    _JD_MIN = -784350574879
    _JD_MAX = 784354017364
    _JD_EPOCH = 2440588  # 1970-01-01T00:00:00Z

    _MSEC_PER_SEC = 1000
    _SEC_PER_MIN = 60
    _MIN_PER_HOUR = 60
    _MSEC_PER_DAY = 86_400_000

    @staticmethod
    def parse_julian_date(jd: int, context: SBValue) -> (SBValue, SBValue, SBValue):
        if jd < DateTimeHelpers._JD_MIN or jd > DateTimeHelpers._JD_MAX:
            return None, None, None

        # The below code is from the Qt sources:

        # Math from The Calendar FAQ at http://www.tondering.dk/claus/cal/julperiod.php
        # This formula is correct for all julian days, when using mathematical integer
        # division (round to negative infinity), not c++11 integer division (round to zero)

        a = jd + 32044
        b = DateTimeHelpers._q_div(4 * a + 3, 146097)
        c = a - DateTimeHelpers._q_div(146097 * b, 4)

        d = DateTimeHelpers._q_div(4 * c + 3, 1461)
        e = c - DateTimeHelpers._q_div(1461 * d, 4)
        m = DateTimeHelpers._q_div(5 * e + 2, 153)

        y = 100 * b + d - 4800 + DateTimeHelpers._q_div(m, 10)

        # Adjust for no year 0
        year = y if y > 0 else y - 1
        month = m + 3 - 12 * DateTimeHelpers._q_div(m, 10)
        day = e - DateTimeHelpers._q_div(153 * m + 2, 5) + 1

        d_year = SBData.CreateDataFromInt(year)
        d_month = SBData.CreateDataFromInt(month)
        d_day = SBData.CreateDataFromInt(day)

        type_int = context.GetTarget().GetBasicType(eBasicTypeInt)

        return (context.CreateValueFromData(DateTimeHelpers.PROP_YEAR, d_year, type_int),
                context.CreateValueFromData(DateTimeHelpers.PROP_MONTH, d_month, type_int),
                context.CreateValueFromData(DateTimeHelpers.PROP_DAY, d_day, type_int))

    @staticmethod
    def _q_div(a: int, b: int) -> int:
        return math.floor(a / b)

    @staticmethod
    def parse_time(mds: int, context: SBValue) -> (SBValue, SBValue, SBValue, SBValue):
        if mds == -1:
            return None, None, None, None

        (mds, milliseconds) = divmod(mds, DateTimeHelpers._MSEC_PER_SEC)
        (mds, seconds) = divmod(mds, DateTimeHelpers._SEC_PER_MIN)
        (hours, minutes) = divmod(mds, DateTimeHelpers._MIN_PER_HOUR)

        d_hours = SBData.CreateDataFromInt(hours)
        d_minutes = SBData.CreateDataFromInt(minutes)
        d_seconds = SBData.CreateDataFromInt(seconds)
        d_milliseconds = SBData.CreateDataFromInt(milliseconds)

        type_int = context.GetTarget().GetBasicType(eBasicTypeInt)

        return (
            context.CreateValueFromData(DateTimeHelpers.PROP_HOURS, d_hours, type_int),
            context.CreateValueFromData(DateTimeHelpers.PROP_MINUTES, d_minutes, type_int),
            context.CreateValueFromData(DateTimeHelpers.PROP_SECONDS, d_seconds, type_int),
            context.CreateValueFromData(DateTimeHelpers.PROP_MILLISECONDS, d_milliseconds, type_int)
        )

    @staticmethod
    def msecs_to_date_time(msecs: int) -> (int, int):
        jd = DateTimeHelpers._JD_EPOCH

        if msecs >= DateTimeHelpers._MSEC_PER_DAY or msecs <= -DateTimeHelpers._MSEC_PER_DAY:
            jd += int(msecs / DateTimeHelpers._MSEC_PER_DAY)
            msecs %= DateTimeHelpers._MSEC_PER_DAY

        if msecs < 0:
            ds = DateTimeHelpers._MSEC_PER_DAY - msecs - 1
            jd -= int(ds / DateTimeHelpers._MSEC_PER_DAY)
            ds = ds % DateTimeHelpers._MSEC_PER_DAY
            ds = DateTimeHelpers._MSEC_PER_DAY - ds - 1
        else:
            ds = msecs

        return jd, ds
