from typing import Iterable, Tuple

from gdb import Value, parse_and_eval
from .baseprinter import StringAndStructurePrinter
from .qstring import QStringPrinter


class QDirPrinter(StringAndStructurePrinter):
    PROP_ABSOLUTE_PATH = 'absolutePath'
    PROP_EXISTS = 'exists'

    def to_string(self) -> str:
        absolute_path = parse_and_eval(f'((QDir*){int(self._valobj.address)})->absolutePath()')
        printer = QStringPrinter(absolute_path)
        text = printer.to_string()
        return text

    def children(self) -> Iterable[Tuple[str, Value]]:
        addr = int(self._valobj.address)
        absolute_path = parse_and_eval(f'((QDir*){addr})->absolutePath()')
        exists = parse_and_eval(f'((QDir*){addr})->exists()')
        yield QDirPrinter.PROP_ABSOLUTE_PATH, absolute_path
        yield QDirPrinter.PROP_EXISTS, exists
