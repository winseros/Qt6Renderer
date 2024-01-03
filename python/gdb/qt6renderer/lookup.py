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
from .qhostaddress import QHostAddressPrinter
from .qlocale import QLocalePrinter
from .qlist import QListPrinter
from .qstring import QStringPrinter
from .qtemporarydir import QTemporaryDirPrinter
from .qtime import QTimePrinter
from .qurl import QUrlPrinter
from .quuid import QUuidPrinter
from .qvariant import QVariantPrinter
from .qt import qt, QtVersion
from .helpers import has_cpp_type, has_cpp_generic_type


def qt6_lookup(valobj: Value):
    if qt().version() < QtVersion.V6_0_0:
        return None

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
    elif has_cpp_generic_type(valobj, 'QHash'):
        return QHashPrinter(valobj)
    elif (has_cpp_generic_type(valobj, 'QHash', '::iterator')
          or has_cpp_generic_type(valobj, 'QHash', '::const_iterator')):
        return QHashIteratorPrinter(valobj)
    elif has_cpp_type(valobj, 'QHostAddress'):
        return QHostAddressPrinter(valobj)
    elif has_cpp_type(valobj, 'QLocale'):
        return QLocalePrinter(valobj)
    elif has_cpp_generic_type(valobj, 'QList'):
        return QListPrinter(valobj)
    elif has_cpp_type(valobj, 'QString'):
        return QStringPrinter(valobj)
    elif has_cpp_type(valobj, 'QTemporaryDir'):
        return QTemporaryDirPrinter(valobj)
    elif has_cpp_type(valobj, 'QTime'):
        return QTimePrinter(valobj)
    elif has_cpp_type(valobj, 'QUrl'):
        return QUrlPrinter(valobj)
    elif has_cpp_type(valobj, 'QUuid'):
        return QUuidPrinter(valobj)
    elif has_cpp_type(valobj, 'QVariant'):
        return QVariantPrinter(valobj)

    return None
