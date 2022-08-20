from lldb import SBTarget, SBValue, SBType, SBModule, SBExpressionOptions


class QtHelpers:
    def __init__(self, target: SBTarget):
        self._target = target

    def qtVersionAndNamespace(self):
        for func in self._target.FindFunctions('qVersion'):
            name = func.GetSymbol().GetName()
            if name.endswith('()'):
                name = name[:-2]
            if name.count(':') > 2:
                continue

            qtNamespace = name[:name.find('qVersion')]
            self.qtNamespace = lambda: qtNamespace

            options = SBExpressionOptions()
            res = self._target.EvaluateExpression(name + '()', options)

            if not res.IsValid() or not res.GetType().IsPointerType():
                exp = '((const char*())%s)()' % name
                res = self._target.EvaluateExpression(exp, options)

            if not res.IsValid() or not res.GetType().IsPointerType():
                exp = '((const char*())_Z8qVersionv)()'
                res = self._target.EvaluateExpression(exp, options)

            if not res.IsValid() or not res.GetType().IsPointerType():
                continue

            version = str(res)
            if version.count('.') != 2:
                continue

            version.replace("'", '"')  # Both seem possible
            version = version[version.find('"') + 1:version.rfind('"')]

            (major, minor, patch) = version.split('.')
            qtVersion = 0x10000 * int(major) + 0x100 * int(minor) + int(patch)
            self.qtVersion = lambda: qtVersion

            funcs = self._target.FindFunctions('QObject::customEvent')
            if len(funcs):
                symbol = funcs[0].GetSymbol()
                self.qtCustomEventFunc = symbol.GetStartAddress().GetLoadAddress(self._target)

            funcs = self._target.FindFunctions('QObject::property')
            if len(funcs):
                symbol = funcs[0].GetSymbol()
                self.qtPropertyFunc = symbol.GetStartAddress().GetLoadAddress(self._target)
            return (qtNamespace, qtVersion)

        return ('', 0x50200)

    def qtNamespace(self):
        return self.qtVersionAndNamespace()[0]

    def qtVersion(self):
        self.qtVersionAndNamespace()
        return self.qtVersionAndNamespace()[1]

    def evaluate_bool(valobj: SBValue, getter: str):
        target = valobj.GetTarget()
        var_name = valobj.GetName()

        val = target.EvaluateExpression(f'{var_name}.{getter}()')
        named_val = valobj.CreateValueFromData(getter, val.GetData(), val.GetType())
        return named_val


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

        (endianness, pointer_size, type_int) = DateTimeHelpers._get_context_info(context)

        d_year = SBData.CreateDataFromSInt32Array(endianness, pointer_size, [year])
        d_month = SBData.CreateDataFromSInt32Array(endianness, pointer_size, [month])
        d_day = SBData.CreateDataFromSInt32Array(endianness, pointer_size, [day])

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

        (endianness, pointer_size, type_int) = DateTimeHelpers._get_context_info(context)

        d_hours = SBData.CreateDataFromSInt32Array(endianness, pointer_size, [hours])
        d_minutes = SBData.CreateDataFromSInt32Array(endianness, pointer_size, [minutes])
        d_seconds = SBData.CreateDataFromSInt32Array(endianness, pointer_size, [seconds])
        d_milliseconds = SBData.CreateDataFromSInt32Array(endianness, pointer_size, [milliseconds])

        return (
            context.CreateValueFromData(DateTimeHelpers.PROP_HOURS, d_hours, type_int),
            context.CreateValueFromData(DateTimeHelpers.PROP_MINUTES, d_minutes, type_int),
            context.CreateValueFromData(DateTimeHelpers.PROP_SECONDS, d_seconds, type_int),
            context.CreateValueFromData(DateTimeHelpers.PROP_MILLISECONDS, d_milliseconds, type_int)
        )

    @staticmethod
    def msecs_to_date_time(msecs: int) -> (int, int):
        jd = DateTimeHelpers._JD_EPOCH
        ds = 0

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

    @staticmethod
    def _get_context_info(context: SBValue):
        process = context.GetProcess()
        endianness = process.GetByteOrder()
        pointer_size = process.GetAddressByteSize()
        target = context.GetTarget()
        type_int = target.GetBasicType(eBasicTypeInt)

        return (endianness, pointer_size, type_int)


class TypeHelpers:
    @staticmethod
    def read_template_types(module: SBModule, native_type: SBType, count: int):
        start_index = native_type.name.find('<')

        result = []
        if start_index < 0:
            return result

        for i in range(count):
            type_name = TypeHelpers._read_type_name(native_type.name, start_index + 1)
            type_name = TypeHelpers._normalize_type_name(type_name)
            sb_type = module.FindFirstType(type_name)
            result.append(sb_type)
            start_index += len(type_name) + 1

        return result

    @staticmethod
    def _read_type_name(name: str, start_at: int) -> str:
        result = ''
        inner_types = 0
        for i in range(start_at, len(name)):
            char = name[i]
            if inner_types == 0 and (char == ',' or char == '>'):
                return result.strip()
            if char == '<':
                inner_types += 1
            elif char == '>':
                inner_types -= 1
            result += char
        raise 'Incorrect type name'

    @staticmethod
    def _normalize_type_name(type_name: str) -> str:
        # make 'type_name' from, say, 'enum type_name'
        start_index = type_name.find(' ')
        return type_name if start_index < 0 else type_name[start_index + 1:]
