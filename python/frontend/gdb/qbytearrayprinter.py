from backend.gdb.native_types import Value
from core.qbytearrayprovider import QByteArraySummaryProvider
from core.qarraydatapointerstructureprovider import QArayDataPointerStructureProvider
from backend.gdb import GdbValue
from .base import StructureAndSummaryPrinter


class QByteArrayPrinter(StructureAndSummaryPrinter):
    def __init__(self, valobj: Value):
        super().__init__(QArayDataPointerStructureProvider(GdbValue(valobj)),
                         QByteArraySummaryProvider(GdbValue(valobj)))
