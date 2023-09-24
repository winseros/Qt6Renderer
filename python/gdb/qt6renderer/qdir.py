from typing import Iterable, Tuple

from gdb import Value, parse_and_eval
from .baseprinter import StringAndStructurePrinter
from .qstring import QStringPrinter


class QDirPrinter(StringAndStructurePrinter):
    PROP_PATH = 'path'
    PROP_ABSOLUTE_PATH = 'absolutePath'
    PROP_EXISTS = 'exists'

    def to_string(self) -> str:
        for child in self.children():
            printer = QStringPrinter(child[1])
            text = printer.to_string()
            return text

    def children(self) -> Iterable[Tuple[str, Value]]:
        qdir_priv = self._valobj['d_ptr']['d'].dereference()
        file_path = qdir_priv['dirEntry']['m_filePath']
        yield QDirPrinter.PROP_PATH, file_path

        addr = self._valobj.address
        if addr:
            # RValues won't pass here
            addr = int(self._valobj.address)
            absolute_path = parse_and_eval(f'((QDir*){addr})->absolutePath()')
            exists = parse_and_eval(f'((QDir*){addr})->exists()')

            yield QDirPrinter.PROP_ABSOLUTE_PATH, absolute_path
            yield QDirPrinter.PROP_EXISTS, exists
