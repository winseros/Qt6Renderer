from typing import Iterable, Tuple

from gdb import Value
from .baseprinter import StringAndStructurePrinter
from .qstring import QStringPrinter
from .qt import qt, QtVersion


class QTemporaryDirPrinter(StringAndStructurePrinter):
    PROP_PATH_OR_ERROR = 'pathOrError'
    PROP_AUTO_REMOVE = 'autoRemove'
    PROP_SUCCESS = 'success'

    def to_string(self) -> str:
        for child in self.children():
            printer = QStringPrinter(child[1])
            text = printer.to_string()
            return text

    def children(self) -> Iterable[Tuple[str, Value]]:
        priv = self._valobj['d_ptr']
        if qt().version() >= QtVersion.V6_4_0:
            priv = priv.dereference()  # raw pointer since 6.4.0
        else:
            priv = priv['d'].dereference()  # QSharedDataPointer

        yield QTemporaryDirPrinter.PROP_PATH_OR_ERROR, priv['pathOrError']
        yield QTemporaryDirPrinter.PROP_AUTO_REMOVE, priv['autoRemove']
        yield QTemporaryDirPrinter.PROP_SUCCESS, priv['success']
