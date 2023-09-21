from backend.gdb.native_types import Value
from core.qarraydatapointerstructureprovider import QArayDataPointerStructureProvider
from core.qstringprovider import QStringSummaryProvider
from backend.gdb import GdbValue
from .base import StructureAndSummaryPrinter


class QStringPrinter(StructureAndSummaryPrinter):
    def __init__(self, valobj: Value):
        super().__init__(QArayDataPointerStructureProvider(GdbValue(valobj)),
                         QStringSummaryProvider(GdbValue(valobj)))
