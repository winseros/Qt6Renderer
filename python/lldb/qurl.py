from qstring import qstring_unquoted
from abstractsynth import AbstractSynth
from lldb import eBasicTypeInt


def qurl_summary(valobj):
    scheme = qstring_unquoted(valobj.GetChildMemberWithName(QUrlSynth.PROP_SCHEME))
    user_name = qstring_unquoted(valobj.GetChildMemberWithName(QUrlSynth.PROP_USER_NAME))
    password = qstring_unquoted(valobj.GetChildMemberWithName(QUrlSynth.PROP_PASSWORD))
    host = qstring_unquoted(valobj.GetChildMemberWithName(QUrlSynth.PROP_HOST))
    port = valobj.GetChildMemberWithName(QUrlSynth.PROP_PORT).GetValueAsSigned()
    path = qstring_unquoted(valobj.GetChildMemberWithName(QUrlSynth.PROP_PATH))
    query = qstring_unquoted(valobj.GetChildMemberWithName(QUrlSynth.PROP_QUERY))
    fragment = qstring_unquoted(valobj.GetChildMemberWithName(QUrlSynth.PROP_FRAGMENT))

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
    PROP_SCHEME = 'scheme'
    PROP_USER_NAME = 'userName'
    PROP_PASSWORD = 'password'
    PROP_HOST = 'host'
    PROP_PORT = 'port'
    PROP_PATH = 'path'
    PROP_QUERY = 'query'
    PROP_FRAGMENT = 'fragment'

    def get_child_index(self, name: str) -> int:
        if name == QUrlSynth.PROP_SCHEME:
            return 0
        elif name == QUrlSynth.PROP_USER_NAME:
            return 1
        elif name == QUrlSynth.PROP_PASSWORD:
            return 2
        elif name == QUrlSynth.PROP_HOST:
            return 3
        elif name == QUrlSynth.PROP_PORT:
            return 4
        elif name == QUrlSynth.PROP_PATH:
            return 5
        elif name == QUrlSynth.PROP_QUERY:
            return 6
        elif name == QUrlSynth.PROP_FRAGMENT:
            return 7
        else:
            return -1

    def update(self):
        type_qstring = self._valobj.GetFrame().GetModule().FindFirstType('QString')
        type_int = self._valobj.GetTarget().GetBasicType(eBasicTypeInt)

        addr = self._valobj.GetChildMemberWithName('d').GetValueAsUnsigned()
        print(addr)

        port = self._valobj.CreateValueFromAddress(QUrlSynth.PROP_PORT, addr + 4, type_int)
        scheme = self._valobj.CreateValueFromAddress(QUrlSynth.PROP_SCHEME, addr + 8, type_qstring)
        user_name = self._valobj.CreateValueFromAddress(QUrlSynth.PROP_USER_NAME, addr + 32, type_qstring)
        password = self._valobj.CreateValueFromAddress(QUrlSynth.PROP_PASSWORD, addr + 56, type_qstring)
        host = self._valobj.CreateValueFromAddress(QUrlSynth.PROP_HOST, addr + 80, type_qstring)
        path = self._valobj.CreateValueFromAddress(QUrlSynth.PROP_PATH, addr + 104, type_qstring)
        query = self._valobj.CreateValueFromAddress(QUrlSynth.PROP_QUERY, addr + 128, type_qstring)
        fragment = self._valobj.CreateValueFromAddress(QUrlSynth.PROP_FRAGMENT, addr + 152, type_qstring)

        self._values = [scheme, user_name, password, host, port, path, query, fragment]

        return False

