from gdb import Value
from .qatomicint import QAtomicIntPrinter
from .qbitarray import QBitArrayPrinter
from .qbytearray import QByteArrayPrinter
from .qchar import QCharPrinter
from .qdate import QDatePrinter
from .qdatetime import QDateTimePrinter
from .qdir import QDirPrinter
from .qevent import QEventPrinter
from .qfile import QFilePrinter
from .qfileinfo import QFileInfoPrinter
from .qflags import QFlagsPrinter
from .qhash import QHashPrinter, QHashIteratorPrinter
from .qstring import QStringPrinter
from .helpers import has_cpp_type, has_cpp_generic_type


def qt6_lookup(valobj: Value):
    if has_cpp_type(valobj, 'QAtomicInt'):
        return QAtomicIntPrinter(valobj)
    elif has_cpp_type(valobj, 'QBitArray'):
        return QBitArrayPrinter(valobj)
    elif has_cpp_type(valobj, 'QByteArray'):
        return QByteArrayPrinter(valobj)
    elif has_cpp_type(valobj, 'QChar'):
        return QCharPrinter(valobj)
    elif has_cpp_type(valobj, 'QDate'):
        return QDatePrinter(valobj)
    elif has_cpp_type(valobj, 'QDateTime'):
        return QDateTimePrinter(valobj)
    elif has_cpp_type(valobj, 'QDir'):
        return QDirPrinter(valobj)
    elif has_cpp_type(valobj, 'QEvent'):
        return QEventPrinter(valobj)
    elif has_cpp_type(valobj, 'QFile'):
        return QFilePrinter(valobj)
    elif has_cpp_type(valobj, 'QFileInfo'):
        return QFileInfoPrinter(valobj)
    elif has_cpp_generic_type(valobj, 'QFlags'):
        return QFlagsPrinter(valobj)
    elif (has_cpp_generic_type(valobj, 'QHash')
          or has_cpp_generic_type(valobj, 'QHash', '::iterator')
          or has_cpp_generic_type(valobj, 'QHash', '::const_iterator')):
        return QHashIteratorPrinter(valobj)
    elif has_cpp_type(valobj, 'QString'):
        return QStringPrinter(valobj)

    return None
