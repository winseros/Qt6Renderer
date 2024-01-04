from typing import Iterable, Tuple

from gdb import Value, parse_and_eval
from .baseprinter import StringAndStructurePrinter
from .qstring import QStringPrinter


class QFileInfoPrinter(StringAndStructurePrinter):
    PROP_FILE_PATH = 'filePath'
    PROP_CACHING = 'caching'
    PROP_EXISTS = 'exists'
    PROP_IS_DIR = 'isDir'
    PROP_IS_EXECUTABLE = 'isExecutable'
    PROP_IS_FILE = 'isFile'
    PROP_IS_HIDDEN = 'isHidden'
    PROP_IS_READABLE = 'isReadable'
    PROP_IS_RELATIVE = 'isRelative'
    PROP_IS_SYMLINK = 'isSymLink'
    PROP_IS_WRITABLE = 'isWritable'

    def to_string(self) -> str:
        for child in self.children():
            printer = QStringPrinter(child[1])
            text = printer.to_string()
            return text

    def children(self) -> Iterable[Tuple[str, Value]]:
        fi_priv = self._valobj['d_ptr']['d'].dereference()
        file_path = fi_priv['fileEntry']['m_filePath']

        yield QFileInfoPrinter.PROP_FILE_PATH, file_path

        if self._valobj.address:
            addr = int(self._valobj.address)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_CACHING)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_EXISTS)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_IS_DIR)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_IS_EXECUTABLE)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_IS_FILE)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_IS_HIDDEN)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_IS_READABLE)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_IS_RELATIVE)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_IS_SYMLINK)
            yield QFileInfoPrinter._get_method_prop(addr, QFileInfoPrinter.PROP_IS_WRITABLE)

    @staticmethod
    def _get_method_prop(address: int, prop: str):
        value = parse_and_eval(f'((QFileInfo*){address})->{prop}()')
        return prop, value
