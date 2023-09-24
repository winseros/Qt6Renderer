from typing import Iterable, Tuple

from gdb import Value, parse_and_eval, lookup_type
from .baseprinter import StringAndStructurePrinter
from .qstring import QStringPrinter


class QFilePrinter(StringAndStructurePrinter):
    PROP_FILE_NAME = 'fileName'
    PROP_EXISTS = 'exists'

    def to_string(self) -> str:
        for child in self.children():
            printer = QStringPrinter(child[1])
            text = printer.to_string()
            return text

    def children(self) -> Iterable[Tuple[str, Value]]:
        t_file_priv_p = lookup_type('QFilePrivate').pointer()

        file_priv = self._valobj['d_ptr']['d'].cast(t_file_priv_p).dereference()
        yield QFilePrinter.PROP_FILE_NAME, file_priv['fileName']

        if self._valobj.address:
            addr = int(self._valobj.address)
            exists = parse_and_eval(f'((QFile*){addr})->exists()')
            yield QFilePrinter.PROP_EXISTS, exists
