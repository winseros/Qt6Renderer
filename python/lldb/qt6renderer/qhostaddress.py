from lldb import SBValue, SBError, eBasicTypeUnsignedInt, eBasicTypeSignedChar
from .qshareddata import QSharedData


def qhostaddress_summary(valobj: SBValue):
    d = valobj.GetChildMemberWithName('d').GetChildMemberWithName('d')

    priv = QHostAddressPrivate(d)
    protocol = priv.protocol().GetValueAsUnsigned()

    text = '(Invalid)'
    if protocol == 0:
        text = _format_as_v4(priv.data_v4())
    elif protocol == 1:
        text = _format_as_v6(priv.data_v6())
    return text


def _format_as_v4(ipv4: SBValue) -> str:
    a4 = ipv4.data.uint32s[0]

    a4, n4 = divmod(a4, 256)
    a4, n3 = divmod(a4, 256)
    a4, n2 = divmod(a4, 256)
    a4, n1 = divmod(a4, 256)

    return f'{n1}.{n2}.{n3}.{n4}'


def _format_as_v6(ipv6: SBValue) -> str:
    a6 = ipv6.data.uint8s

    text = ''
    for i in range(0, len(a6), 2):
        if i > 0:
            text += ':'
        text += f'{a6[i]:02x}{a6[i + 1]:02x}'
    return text


class QHostAddressPrivate(QSharedData):
    def __init__(self, pointer: SBValue):
        super().__init__(pointer)
        self.add_named_type_field('scope_id', 'QString')
        self.add_sb_type_field('data_v6', pointer.target.FindFirstType('quint8').GetArrayType(16))
        self.add_named_type_field('data_v4', 'quint32')
        self.add_named_type_field('protocol', 'qint8')

    def data_v6(self) -> SBValue:
        pass

    def data_v4(self) -> SBValue:
        pass

    def protocol(self) -> SBValue:
        pass
