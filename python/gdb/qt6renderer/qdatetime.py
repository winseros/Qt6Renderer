from typing import Iterable, Tuple

from gdb import Value, lookup_type
from .baseprinter import StringAndStructurePrinter
from .helpers import DateTimeHelpers


class QDateTimePrinter(StringAndStructurePrinter):
    PROP_SPEC = 'spec'
    PROP_OFFSET_FROM_UTC = 'offset_from_utc'
    PROP_RAW_DATA = 'raw_data'

    def to_string(self) -> str:
        children = list(self.children())
        if len(children) < 2:
            return DateTimeHelpers.VAL_INVALID

        year = children[0][1]
        month = children[1][1]
        day = children[2][1]
        hour = children[3][1]
        minute = children[4][1]
        second = children[5][1]
        msecond = children[6][1]
        offset = children[7][1]

        return f'{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}.{msecond:03d}{QDateTimePrinter.offset_format(int(offset))}'

    def children(self) -> Iterable[Tuple[str, Value]]:
        data = self._valobj['d']
        status = data['data']['status']

        if status & 0x01:
            data = data['data']
            msecs = data['msecs']
            status = data['status']
            is_valid = status & 0x08
            offset_from_utc = 0
        else:
            d_ptr_value = data['d']

            type_int32_ptr = lookup_type('int').pointer()
            type_int64_ptr = lookup_type('long long').pointer()

            # +x here and below is in the "pointer sizes"
            # i.e. int32_ptr+x means address+(x * sizeof pointer) in the real address space
            status = (d_ptr_value.cast(type_int32_ptr) + 1).dereference()
            msecs = (d_ptr_value.cast(type_int64_ptr) + 1).dereference()
            offset_from_utc = (d_ptr_value.cast(type_int32_ptr) + 2 + int(type_int32_ptr.sizeof / 4)).dereference()

            is_valid = True

        spec = (status & 0x30) >> 4
        spec = spec.cast(lookup_type('Qt::TimeSpec'))

        if is_valid:
            jd, ds = DateTimeHelpers.msecs_to_date_time(int(msecs))
            year, month, day = DateTimeHelpers.parse_julian_date(jd)
            hours, minutes, seconds, milliseconds = DateTimeHelpers.parse_time(ds)

            yield DateTimeHelpers.PROP_YEAR, year
            yield DateTimeHelpers.PROP_MONTH, month
            yield DateTimeHelpers.PROP_DAY, day
            yield DateTimeHelpers.PROP_HOURS, hours
            yield DateTimeHelpers.PROP_MINUTES, minutes
            yield DateTimeHelpers.PROP_SECONDS, seconds
            yield DateTimeHelpers.PROP_MILLISECONDS, milliseconds
            yield QDateTimePrinter.PROP_OFFSET_FROM_UTC, offset_from_utc
            yield QDateTimePrinter.PROP_SPEC, spec
            yield QDateTimePrinter.PROP_RAW_DATA, data
        else:
            yield DateTimeHelpers.PROP_INVALID, True

    @staticmethod
    def offset_format(seconds: int) -> str:
        text = '+' if seconds >= 0 else '-'

        (hours, seconds) = divmod(seconds, 3600)
        (minutes, seconds) = divmod(seconds, 60)

        text += f'{abs(hours):02d}'
        text += ':' + f'{abs(minutes):02d}'
        if seconds > 0:
            text += ':' + f'{abs(seconds):02d}'

        return text
