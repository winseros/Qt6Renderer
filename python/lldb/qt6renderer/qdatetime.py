from lldb import SBValue, SBData, SBError, eByteOrderLittle, eBasicTypeInt, eBasicTypeLongLong
from .datetimehelpers import DateTimeHelpers
from .abstractsynth import AbstractSynth
from .syntheticstruct import SyntheticStruct


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
        return f'{year}-{month:02d}-{day:02d}T{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}{offset_format(offset_from_utc)}'
    else:
        return '(Invalid)'


def offset_format(seconds: int) -> str:
    text = '+' if seconds >= 0 else '-'

    (hours, seconds) = divmod(seconds, 3600)
    (minutes, seconds) = divmod(seconds, 60)

    text += f'{abs(hours):02d}'
    text += ':' + f'{abs(minutes):02d}'
    if seconds > 0:
        text += ':' + f'{abs(seconds):02d}'

    return text


class QDateTimeSynth(AbstractSynth):
    PROP_SPEC = 'spec'
    PROP_OFFSET_FROM_UTC = 'offset_from_utc'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)

        process = valobj.GetProcess()
        self._endianness = process.GetByteOrder()
        self._pointer_size = process.GetAddressByteSize()

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
        else:
            return -1

    def update(self):
        d = self._valobj.GetChildMemberWithName('d')
        status = d.data.sint8[0]

        if status & 0x01:
            data = d.GetChildMemberWithName('data')
            msecs = data.GetChildMemberWithName('msecs').GetValueAsSigned()
            status = data.GetChildMemberWithName('status').GetValueAsUnsigned()
            is_valid = status & 0x08
            offset_from_utc = 0
        else:
            d_d = d.GetChildMemberWithName('d')
            private = QDateTimePrivate(d_d)
            status = private.status().GetValueAsSigned()
            msecs = private.msecs().GetValueAsSigned()
            offset_from_utc = private.offset_from_utc().GetValueAsSigned()
            is_valid = True

        spec = (status & 0x30) >> 4

        if is_valid:
            jd, ds = DateTimeHelpers.msecs_to_date_time(msecs)
            (year, month, day) = DateTimeHelpers.parse_julian_date(jd, self._valobj)
            (hours, minutes, seconds, milliseconds) = DateTimeHelpers.parse_time(ds, self._valobj)

            p_offset_from_utc = self.make_offset_from_utc(offset_from_utc)
            p_spec = self.make_spec(spec)

            self._values = [year, month, day, hours, minutes, seconds, milliseconds, p_offset_from_utc, p_spec]

        return False

    def make_offset_from_utc(self, offset_from_utc: int) -> SBValue:
        return self._valobj.CreateValueFromData(QDateTimeSynth.PROP_OFFSET_FROM_UTC,
                                                SBData.CreateDataFromSInt32Array(self._endianness,
                                                                                 self._pointer_size,
                                                                                 [offset_from_utc]),
                                                self._valobj.GetTarget().GetBasicType(
                                                    eBasicTypeInt))

    def make_spec(self, spec: int) -> SBValue:
        return self._valobj.CreateValueFromExpression(QDateTimeSynth.PROP_SPEC, '(Qt::TimeSpec)' + str(spec))


class QDateTimePrivate(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_field('status', eBasicTypeInt)
        self.add_field('msecs', eBasicTypeLongLong)
        self.add_field('offset_from_utc', eBasicTypeInt)

    def status(self) -> SBValue:
        pass

    def msecs(self) -> SBValue:
        pass

    def offset_from_utc(self) -> SBValue:
        pass
