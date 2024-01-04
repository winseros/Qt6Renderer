from typing import Iterable, Tuple

from gdb import Value
from .baseprinter import StringAndStructurePrinter
from .qstring import QStringPrinter


class QUrlPrinter(StringAndStructurePrinter):
    PROP_SCHEME = 'scheme'
    PROP_USER_NAME = 'userName'
    PROP_PASSWORD = 'password'
    PROP_HOST = 'host'
    PROP_PORT = 'port'
    PROP_PATH = 'path'
    PROP_QUERY = 'query'
    PROP_FRAGMENT = 'fragment'

    def to_string(self) -> str:
        children = list(self.children())
        scheme = QStringPrinter(children[0][1]).to_string()
        userName = QStringPrinter(children[1][1]).to_string()
        password = QStringPrinter(children[2][1]).to_string()
        host = QStringPrinter(children[3][1]).to_string()
        port = int(children[4][1])
        path = QStringPrinter(children[5][1]).to_string()
        query = QStringPrinter(children[6][1]).to_string()
        fragment = QStringPrinter(children[7][1]).to_string()

        url = scheme + '://' if scheme else ''
        if userName: url += userName
        if password: url += ':' + password
        if userName or password: url += '@'
        if host: url += host
        if port > 0: url += ':' + str(port)
        if path: url += path
        if query: url += '?' + query
        if fragment: url += '#' + fragment

        return url

    def children(self) -> Iterable[Tuple[str, Value]]:
        d = self._valobj['d'].dereference()

        yield QUrlPrinter.PROP_SCHEME, d['scheme']
        yield QUrlPrinter.PROP_USER_NAME, d['userName']
        yield QUrlPrinter.PROP_PASSWORD, d['password']
        yield QUrlPrinter.PROP_HOST, d['host']
        yield QUrlPrinter.PROP_PORT, d['port']
        yield QUrlPrinter.PROP_PATH, d['path']
        yield QUrlPrinter.PROP_QUERY, d['query']
        yield QUrlPrinter.PROP_FRAGMENT, d['fragment']
