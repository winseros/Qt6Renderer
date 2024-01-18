from lldb import eBasicTypeBool, eBasicTypeInt, eBasicTypeUnsignedInt, eBasicTypeLongLong, eBasicTypeUnsignedLongLong, \
    eBasicTypeDouble, eBasicTypeLong, eBasicTypeShort, eBasicTypeChar, eBasicTypeUnsignedLong, eBasicTypeUnsignedShort, \
    eBasicTypeUnsignedChar, eBasicTypeFloat, eBasicTypeSignedChar, SBValue, SBProcess, SBError

from .abstractsynth import AbstractSynth


class QVariantSynth(AbstractSynth):
    PROP_VALUE = 'value'

    _builtins_a = [eBasicTypeBool, eBasicTypeInt, eBasicTypeUnsignedInt, eBasicTypeLongLong,
                   eBasicTypeUnsignedLongLong, eBasicTypeDouble]
    _builtins_d = [eBasicTypeLong, eBasicTypeShort, eBasicTypeChar, eBasicTypeUnsignedLong, eBasicTypeUnsignedShort,
                   eBasicTypeUnsignedChar, eBasicTypeFloat]

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        self._type_int = valobj.GetTarget().GetBasicType(eBasicTypeInt)
        self._type_cstr = valobj.GetTarget().GetBasicType(eBasicTypeChar).GetPointerType()
        self._type_ptr = valobj.GetTarget().GetBasicType(eBasicTypeUnsignedLongLong).GetPointerType()

    def get_child_index(self, name: str) -> int:
        if name == self.PROP_VALUE:
            return 0
        else:
            return -1

    def update(self) -> bool:
        d = self._valobj.GetChildMemberWithName('d')
        packed_type = d.GetChildMemberWithName('packedType')
        p_data = packed_type.GetValueAsUnsigned() << 2

        # QMetaTypeInterface
        # ushort revision
        # ushort alignment
        # uint size
        # uint flags
        # mutable QBasicAtomicInt typeId
        type_id = self._valobj.CreateValueFromAddress('type_id', p_data + 12, self._type_int).GetValueAsUnsigned()

        if 0 < type_id <= 6:
            self._internal(d, self._builtins_a[type_id - 1])
        elif type_id == 31:
            self._void_star(d)
        elif 32 <= type_id <= 38:
            self._internal(d, self._builtins_d[type_id - 32])
        elif type_id == 40:
            self._internal(d, eBasicTypeSignedChar)
        else:
            self._external(d, p_data)

        if not len(self._values):
            self._default(p_data)

        return False

    def _void_star(self, d: SBValue):
        t = self._valobj.target.FindFirstType('void').GetPointerType()
        value = self._valobj.CreateValueFromAddress(self.PROP_VALUE, d.load_addr, t)
        self._values = [value, d]

    def _internal(self, d: SBValue, basic_type: int):
        t = self._valobj.target.GetBasicType(basic_type)
        value = self._valobj.CreateValueFromAddress(self.PROP_VALUE, d.load_addr, t)
        self._values = [value]

    def _external(self, d: SBValue, p_data: int):
        p_type_name = self._valobj.CreateValueFromAddress('t', p_data + 24, self._type_ptr).GetValueAsUnsigned()
        type_name = self._read_cstr(self._valobj.process, p_type_name)
        t = self._valobj.target.FindFirstType(type_name)
        is_shared = d.GetChildMemberWithName('is_shared').GetValueAsUnsigned()
        if is_shared:
            addr = self._valobj.CreateValueFromAddress('ptr', d.load_addr, self._type_ptr).GetValueAsUnsigned()
        else:
            addr = d.load_addr
        value = self._valobj.CreateValueFromAddress(self.PROP_VALUE, addr, t)
        self._values = [value]

    @staticmethod
    def _read_cstr(process: SBProcess, addr: int):
        err = SBError()
        text = process.ReadCStringFromMemory(addr, 256, err)
        if err.Fail():
            raise err.GetCString()
        return text

    def _default(self, p_data: int):
        name = self._valobj.CreateValueFromAddress('type', p_data + 24, self._type_cstr)
        self._values = [name]

        n = self._valobj.GetNumChildren()
        for i in range(n):
            self._values.append(self._valobj.GetChildAtIndex(i))
