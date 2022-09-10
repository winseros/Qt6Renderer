from abstractsynth import AbstractSynth
from lldb import SBValue, eBasicTypeUnsignedLongLong


class QLocaleSynth(AbstractSynth):
    PROP_LANG = 'language'
    PROP_SCRIPT = 'script'
    PROP_TERRITORY = 'territory'
    PROP_NUM_OPTS = 'num_opts'

    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
        t = valobj.GetTarget()
        m = valobj.GetFrame().GetModule()
        self._type_ulong = t.GetBasicType(eBasicTypeUnsignedLongLong)
        self._type_lang = m.FindFirstType(valobj.type.name + '::Language')
        self._type_script = m.FindTypes(valobj.type.name + '::Script').GetTypeAtIndex(0)
        self._type_territory = m.FindFirstType(valobj.type.name + '::Territory')
        if not self._type_territory.IsValid():
            self._type_territory = m.FindFirstType(valobj.type.name + '::Country')
        self._type_num_opts = m.FindFirstType(valobj.type.name + '::NumberOptions')
        if not self._type_num_opts.IsValid():
            self._type_num_opts = m.FindFirstType(f'QFlags<enum {valobj.type.name}::NumberOption>')
        # self._type_currency_code = t.GetBasicType(eBasicTypeChar).GetArrayType(3)

    def get_child_index(self, name: str) -> int:
        if name == self.PROP_TERRITORY:
            return 0
        if name == self.PROP_LANG:
            return 1
        if name == self.PROP_SCRIPT:
            return 2
        if name == self.PROP_NUM_OPTS:
            return 3

        return -1

    def update(self):
        d = self._valobj.GetChildMemberWithName('d')
        addr = d.GetChildMemberWithName('d').GetValueAsUnsigned()
        p_data = self._valobj.CreateValueFromAddress('data', addr, self._type_ulong).GetValueAsUnsigned()
        num_opts = self._valobj.CreateValueFromAddress('num_opts', addr + 12, self._type_num_opts)

        lang = self._valobj.CreateValueFromAddress(self.PROP_LANG, p_data, self._type_lang)
        script = self._valobj.CreateValueFromAddress(self.PROP_SCRIPT, p_data + 2, self._type_script)
        territory = self._valobj.CreateValueFromAddress(self.PROP_TERRITORY, p_data + 4, self._type_territory)
        # currency_code = self._valobj.CreateValueFromAddress(self.PROP_CURRENCY_CODE, p_data + 117, self._type_currency_code)

        self._values = [territory, lang, script, num_opts, d]

        return True
