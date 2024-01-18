from lldb import SBValue
from .abstractsynth import AbstractSynth
from .syntheticstruct import SyntheticStruct
from .qstring import qstring_summary_no_quotes


def qurl_summary(valobj: SBValue) -> str:
    scheme = qstring_summary_no_quotes(valobj.GetChildMemberWithName(QUrlPrivate.PROP_SCHEME))
    user_name = qstring_summary_no_quotes(valobj.GetChildMemberWithName(QUrlPrivate.PROP_USER_NAME))
    password = qstring_summary_no_quotes(valobj.GetChildMemberWithName(QUrlPrivate.PROP_PASSWORD))
    host = qstring_summary_no_quotes(valobj.GetChildMemberWithName(QUrlPrivate.PROP_HOST))
    port = valobj.GetChildMemberWithName(QUrlPrivate.PROP_PORT).GetValueAsSigned()
    path = qstring_summary_no_quotes(valobj.GetChildMemberWithName(QUrlPrivate.PROP_PATH))
    query = qstring_summary_no_quotes(valobj.GetChildMemberWithName(QUrlPrivate.PROP_QUERY))
    fragment = qstring_summary_no_quotes(valobj.GetChildMemberWithName(QUrlPrivate.PROP_FRAGMENT))

    result = ''
    if scheme:
        result += scheme + '://'
    if user_name:
        result += user_name
    if password:
        result += ':' + password
    if user_name or password:
        result += '@'
    if host:
        result += host
    if port != -1:
        result += ':' + str(port)
    if path:
        result += path
    if query:
        result += '?' + query
    if fragment:
        result += '#' + fragment

    return result


class QUrlSynth(AbstractSynth):

    def get_child_index(self, name: str) -> int:
        if name == QUrlPrivate.PROP_SCHEME:
            return 0
        elif name == QUrlPrivate.PROP_USER_NAME:
            return 1
        elif name == QUrlPrivate.PROP_PASSWORD:
            return 2
        elif name == QUrlPrivate.PROP_HOST:
            return 3
        elif name == QUrlPrivate.PROP_PORT:
            return 4
        elif name == QUrlPrivate.PROP_PATH:
            return 5
        elif name == QUrlPrivate.PROP_QUERY:
            return 6
        elif name == QUrlPrivate.PROP_FRAGMENT:
            return 7
        else:
            return -1

    def update(self) -> bool:
        d = self._valobj.GetChildMemberWithName('d')
        priv = QUrlPrivate(d)

        self._values = [
            priv.scheme(), priv.user_name(), priv.password(),
            priv.host(), priv.port(), priv.path(), priv.query(),
            priv.fragment()
        ]


class QUrlPrivate(SyntheticStruct):
    PROP_SCHEME = 'scheme'
    PROP_USER_NAME = 'userName'
    PROP_PASSWORD = 'password'
    PROP_HOST = 'host'
    PROP_PORT = 'port'
    PROP_PATH = 'path'
    PROP_QUERY = 'query'
    PROP_FRAGMENT = 'fragment'

    def __init__(self, pointer: SBValue):
        super().__init__(pointer)

        self.add_named_type_field('ref', 'QAtomicInt')
        self.add_named_type_field(QUrlPrivate.PROP_PORT, 'int')
        self.add_named_type_field(QUrlPrivate.PROP_SCHEME, 'QString')
        self.add_named_type_field(QUrlPrivate.PROP_USER_NAME, 'QString', 'user_name')
        self.add_named_type_field(QUrlPrivate.PROP_PASSWORD, 'QString')
        self.add_named_type_field(QUrlPrivate.PROP_HOST, 'QString')
        self.add_named_type_field(QUrlPrivate.PROP_PATH, 'QString')
        self.add_named_type_field(QUrlPrivate.PROP_QUERY, 'QString')
        self.add_named_type_field(QUrlPrivate.PROP_FRAGMENT, 'QString')

    def port(self) -> SBValue:
        pass

    def scheme(self) -> SBValue:
        pass

    def user_name(self) -> SBValue:
        pass

    def password(self) -> SBValue:
        pass

    def host(self) -> SBValue:
        pass

    def path(self) -> SBValue:
        pass

    def query(self) -> SBValue:
        pass

    def fragment(self) -> SBValue:
        pass
