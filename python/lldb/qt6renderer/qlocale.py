from lldb import SBValue, SBType, eBasicTypeUnsignedLongLong, eBasicTypeUnsignedInt, eBasicTypeUnsignedShort
from .abstractsynth import AbstractSynth
from .syntheticstruct import SyntheticStruct
from .qshareddatapointer import QSharedDataPointer


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
        locale = QLocale(self._valobj)
        priv = locale.d().d()
        priv_data = priv.data()

        d = self._valobj.GetChildMemberWithName('d').GetChildMemberWithName('d')

        self._values = [priv_data.territory(), priv_data.language(), priv_data.script(), priv.num_opts(), d]

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

        if not type_lang.IsValid():
            type_lang = context.target.GetBasicType(eBasicTypeUnsignedShort)
        if not type_script.IsValid():
            type_script = context.target.GetBasicType(eBasicTypeUnsignedShort)
        if not type_territory.IsValid():
            type_territory = context.target.GetBasicType(eBasicTypeUnsignedShort)

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

        self.add_synthetic_field('data', lambda p: QLocaleData(p, context), pointer=True)
        self.add_named_type_field('ref', 'QBasicAtomicInt')
        self.add_basic_type_field('index', eBasicTypeUnsignedInt)

        type_num_opts = pointer.target.FindFirstType(context.type.name + '::NumberOptions')
        if not type_num_opts.IsValid():
            type_num_opts = pointer.target.FindFirstType(f'QFlags<enum {context.type.name}::NumberOption>')

        self.add_sb_type_field(QLocalePrivate.PROP_NUM_OPTS, type_num_opts)

    def data(self) -> QLocaleData:
        pass

    def num_opts(self) -> SBValue:
        pass


class QLocale(SyntheticStruct):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)

        self.add_synthetic_field('d', lambda p: QSharedDataPointer(p, lambda q: QLocalePrivate(q, pointer)))

    def d(self) -> QSharedDataPointer[QLocalePrivate]:
        pass
