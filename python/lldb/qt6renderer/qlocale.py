from lldb import SBValue, eBasicTypeUnsignedLongLong, eBasicTypeUnsignedInt
from .abstractsynth import AbstractSynth
from .syntheticstruct import SyntheticStruct


class QLocaleSynth(AbstractSynth):
    def get_child_index(self, name: str) -> int:
        if name == QLocaleData.PROP_LANG:
            return 0
        if name == QLocaleData.PROP_SCRIPT:
            return 1
        if name == QLocaleData.PROP_TERRITORY:
            return 2
        if name == QLocalePrivate.PROP_NUM_OPTS:
            return 3

        return -1

    def update(self):
        d = self._valobj.GetChildMemberWithName('d').GetChildMemberWithName('d')
        priv = QLocalePrivate(d, self._valobj)

        self._values = [priv.data().territory(), priv.data().language(), priv.data().script(), priv.num_opts(), d]

        return True


class QLocaleData(SyntheticStruct):
    PROP_LANG = 'language'
    PROP_SCRIPT = 'script'
    PROP_TERRITORY = 'territory'

    def __init__(self, pointer: SBValue, context: SBValue):
        super().__init__(pointer)

        type_lang = context.target.FindFirstType(context.type.name + '::Language')
        type_script = context.target.FindFirstType(context.type.name + '::Script')
        type_territory = context.target.FindFirstType(context.type.name + '::Territory')
        if not type_territory.IsValid():
            type_territory = context.target.FindFirstType(context.type.name + '::Country')

        self.add_sb_type_field(QLocaleData.PROP_LANG, type_lang)
        self.add_sb_type_field(QLocaleData.PROP_SCRIPT, type_script)
        self.add_sb_type_field(QLocaleData.PROP_TERRITORY, type_territory)

    def language(self) -> SBValue:
        pass

    def script(self) -> SBValue:
        pass

    def territory(self) -> SBValue:
        pass


class QLocalePrivate(SyntheticStruct):
    PROP_NUM_OPTS = 'num_opts'

    def __init__(self, pointer: SBValue, context: SBValue):
        super().__init__(pointer)
        self._context = context

        self.add_sb_type_field('p_data', pointer.target.FindFirstType('void').GetPointerType())
        self.add_named_type_field('ref', 'QBasicAtomicInt')
        self.add_basic_type_field('index', eBasicTypeUnsignedInt)

        type_num_opts = context.target.FindFirstType(context.type.name + '::NumberOptions')
        if not type_num_opts.IsValid():
            type_num_opts = context.target.FindFirstType(f'QFlags<enum {context.type.name}::NumberOption>')

        self.add_sb_type_field(QLocalePrivate.PROP_NUM_OPTS, type_num_opts)

    def p_data(self) -> SBValue:
        pass

    def data(self) -> QLocaleData:
        d = QLocaleData(self.p_data(), self._context)
        self.data = lambda: d
        return d

    def num_opts(self) -> SBValue:
        pass
