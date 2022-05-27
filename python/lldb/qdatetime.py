from helpers import DateTimeHelpers
from lldb import SBValue, SBData, SBError, eByteOrderLittle, eBasicTypeLong


def qdatetime_summary(valobj):
    count = valobj.GetNumChildren()
    if count:
        year = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_YEAR).GetValueAsSigned()
        month = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MONTH).GetValueAsSigned()
        day = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_DAY).GetValueAsSigned()
        hours = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_HOURS).GetValueAsSigned()
        minutes = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MINUTES).GetValueAsSigned()
        seconds = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_SECONDS).GetValueAsSigned()
        milliseconds = valobj.GetChildMemberWithName(DateTimeHelpers.PROP_MILLISECONDS).GetValueAsSigned()
        offset_from_utc = valobj.GetChildMemberWithName(QDateTimeSynth.PROP_OFFSET_FROM_UTC).GetValueAsSigned()
        return '{}-{}-{}T{}:{}:{}.{}{}'.format(year, zero_format1(month), zero_format1(day), zero_format1(hours),
                                               zero_format1(minutes), zero_format1(seconds),
                                               zero_format2(milliseconds),
                                               offset_format(offset_from_utc))
    else:
        return '(Invalid)'


def zero_format1(n: int):
    return str(n) if n > 9 else '0{}'.format(n)


def zero_format2(n: int):
    return n if n > 99 \
        else '0{}'.format(n) if n > 9 \
        else '00{}'.format(n)


def offset_format(seconds: int) -> str:
    text = '+' if seconds >= 0 else '-'

    (hours, seconds) = divmod(seconds, 3600)
    (minutes, seconds) = divmod(seconds, 60)

    text += zero_format1(abs(hours))
    text += ':' + zero_format1(abs(minutes))
    if seconds > 0:
        text += ':' + zero_format1(abs(seconds))

    return text


class QDateTimeSynth:
    PROP_SPEC = 'spec'
    PROP_OFFSET_FROM_UTC = 'offsetFromUtc'
    PROP_RAW_DATA = '[raw_data]'

    def __init__(self, valobj: SBValue):
        self._valobj = valobj
        self._values = []

        process = valobj.GetProcess()
        self._endianness = process.GetByteOrder()
        self._pointer_size = process.GetAddressByteSize()

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
        elif name == DateTimeHelpers.PROP_HOURS:
            return 3
        elif name == DateTimeHelpers.PROP_MINUTES:
            return 4
        elif name == DateTimeHelpers.PROP_SECONDS:
            return 5
        elif name == DateTimeHelpers.PROP_MILLISECONDS:
            return 6
        elif name == QDateTimeSynth.PROP_OFFSET_FROM_UTC:
            return 7
        elif name == QDateTimeSynth.PROP_SPEC:
            return 8
        elif name == QDateTimeSynth.PROP_RAW_DATA:
            return 9
        else:
            return -1

    def get_child_at_index(self, index: int) -> SBValue:
        return self._values[index]

    def get_value(self):
        return self._valobj

    def update(self):
        data = self._valobj.GetChildMemberWithName('d')
        status = data.GetData().sint8[0]

        if status & 0x01:
            data = data.GetChildMemberWithName('data')
            msecs = data.GetChildMemberWithName('msecs').GetValueAsUnsigned()
            status = data.GetChildMemberWithName('status').GetValueAsSigned()
            is_valid = status & 0x08
            offset_from_utc = 0
        else:
            d_ptr_value = data.GetChildMemberWithName('d').GetValueAsUnsigned()
            python_byte_order = 'little' if self._endianness == eByteOrderLittle else 'big'

            process = self._valobj.GetProcess()

            err = SBError()
            b_status = process.ReadMemory(d_ptr_value + 4, 4, err)
            status = int.from_bytes(b_status, python_byte_order)

            b_msecs = process.ReadMemory(d_ptr_value + 8, self._pointer_size, err)
            msecs = int.from_bytes(b_msecs, python_byte_order)

            b_offset_from_utc = process.ReadMemory(d_ptr_value + 8 + self._pointer_size, 4, err)
            offset_from_utc = int.from_bytes(b_offset_from_utc, python_byte_order, signed=True)
            is_valid = True

        spec = (status & 0x30) >> 4

        if is_valid:
            jd, ds = DateTimeHelpers.msecs_to_date_time(msecs)
            (year, month, day) = DateTimeHelpers.parse_julian_date(jd, self._valobj)
            (hours, minutes, seconds, milliseconds) = DateTimeHelpers.parse_time(ds, self._valobj)

            p_offset_from_utc = self.make_offset_from_utc(offset_from_utc)
            p_spec = self.make_spec(spec)
            raw_data = self._valobj.CreateValueFromData(QDateTimeSynth.PROP_RAW_DATA, data.GetData(), data.GetType())

            self._values = [year, month, day, hours, minutes, seconds, milliseconds, p_offset_from_utc, p_spec,
                            raw_data]

        return False

    def make_offset_from_utc(self, offset_from_utc: int) -> SBValue:
        return self._valobj.CreateValueFromData(QDateTimeSynth.PROP_OFFSET_FROM_UTC,
                                                SBData.CreateDataFromSInt32Array(self._endianness,
                                                                                 self._pointer_size,
                                                                                 [offset_from_utc]),
                                                self._valobj.GetTarget().GetBasicType(
                                                    eBasicTypeLong))

    def make_spec(self, spec: int) -> SBValue:
        return self._valobj.CreateValueFromExpression(QDateTimeSynth.PROP_SPEC, '(Qt::TimeSpec)' + str(spec))
