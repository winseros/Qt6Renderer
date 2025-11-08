from lldb import SBValue
from .qt import qt, QtVersion
from .helpers import has_cpp_type, has_cpp_generic_type
from .qatomicint import qatomicint_summary
from .qbitarray import qbitarray_summary, QBitArraySynth
from .qbytearray import qbytearray_summary, QByteArraySynth
from .qcborvalue import QCborValueSynth
from .qchar import qchar_summary
from .qdate import qdate_summary, QDateSynth
from .qdatetime import qdatetime_summary, QDateTimeSynth
from .qdir import qdir_summary, QDirSynth
from .qevent import QEventSynth
from .qfile import qfile_summary, QFileSynth, QTemporaryFileSynth
from .qfileinfo import qfileinfo_summary, QFileInfoSynth
from .qflags import qflags_summary
from .qhash import qhash_summary, QHashSynth, QHashIteratorSynth
from .qjsonobject import QJsonObjectSynth
from .qjsonvalue import QJsonValueSynth
from .qhostaddress import qhostaddress_summary
from .qlist import qlist_summary, QListSynth
from .qlocale import QLocaleSynth
from .qmap import QMapSynth
from .qscopedpointer import qscopedpointer_summary, QScopedPointerSynth
from .qshareddatapointer import qshareddatapointer_summary, QSharedDataPointerSynth
from .qsharedpointer import qsharedpointer_summary, QSharedPointerSynth
from .qstring import qstring_summary, QStringSynth
from .qtcbor_element import qtcborelement_summaru, QtCborElementSynth
from .qtemporarydir import qtemporarydir_summary, QTemporaryDirSynth
from .qtime import qtime_summary, QTimeSynth
from .qtimezone import qtimezone_summary, QTimeZoneSynth
from .qurl import qurl_summary, QUrlSynth
from .quuid import quuid_summary
from .qvariant import QVariantSynth
from .qweakpointer import qweakpointer_summary, QWeakPointerSynth


def qt6_lookup_summary(valobj: SBValue, internal_dict):
    qt_version = qt().version(valobj.target)
    if not qt_version or qt_version < QtVersion.V6_0_0:
        return None

    if has_cpp_type(valobj, 'QAtomicInt') or has_cpp_type(valobj, 'QBasicAtomicInt'):
        return qatomicint_summary(valobj)
    elif has_cpp_type(valobj, 'QBitArray'):
        return qbitarray_summary(valobj)
    elif has_cpp_type(valobj, 'QByteArray'):
        return qbytearray_summary(valobj)
    elif has_cpp_type(valobj, 'QChar'):
        return qchar_summary(valobj)
    elif has_cpp_type(valobj, 'QDate'):
        return qdate_summary(valobj)
    elif has_cpp_type(valobj, 'QDateTime'):
        return qdatetime_summary(valobj)
    elif has_cpp_type(valobj, 'QDir'):
        return qdir_summary(valobj)
    elif has_cpp_type(valobj, 'QFile') or has_cpp_type(valobj, 'QTemporaryFile'):
        return qfile_summary(valobj)
    elif has_cpp_type(valobj, 'QFileInfo'):
        return qfileinfo_summary(valobj)
    elif has_cpp_generic_type(valobj, 'QFlags'):
        return qflags_summary(valobj)
    elif has_cpp_generic_type(valobj, 'QHash'):
        return qhash_summary(valobj)
    elif has_cpp_type(valobj, 'QHostAddress'):
        return qhostaddress_summary(valobj)
    elif has_cpp_generic_type(valobj, 'QList'):
        return qlist_summary(valobj)
    elif has_cpp_generic_type(valobj, 'QScopedPointer'):
        return qscopedpointer_summary(valobj)
    elif has_cpp_generic_type(valobj, 'QSharedDataPointer'):
        return qshareddatapointer_summary(valobj)
    elif has_cpp_generic_type(valobj, 'QSharedPointer'):
        return qsharedpointer_summary(valobj)
    elif has_cpp_type(valobj, 'QString'):
        return qstring_summary(valobj)
    elif has_cpp_type(valobj, 'QtCbor::Element'):
        return qtcborelement_summaru(valobj)
    elif has_cpp_type(valobj, 'QTemporaryDir'):
        return qtemporarydir_summary(valobj)
    elif has_cpp_type(valobj, 'QTime'):
        return qtime_summary(valobj)
    elif has_cpp_type(valobj, 'QTimeZone'):
        return qtimezone_summary(valobj)
    elif has_cpp_type(valobj, 'QUrl'):
        return qurl_summary(valobj)
    elif has_cpp_type(valobj, 'QUuid'):
        return quuid_summary(valobj)
    elif has_cpp_generic_type(valobj, 'QWeakPointer'):
        return qweakpointer_summary(valobj)

    return None


def qt6_lookup_synthetic(valobj: SBValue, internal_dict):
    qt_version = qt().version(valobj.target)
    if not qt_version or qt_version < QtVersion.V6_0_0:
        return None

    if has_cpp_type(valobj, 'QBitArray'):
        return QBitArraySynth(valobj)
    elif has_cpp_type(valobj, 'QByteArray'):
        return QByteArraySynth(valobj)
    elif has_cpp_type(valobj, 'QCborValue'):
        return QCborValueSynth(valobj)
    elif has_cpp_type(valobj, 'QDate'):
        return QDateSynth(valobj)
    elif has_cpp_type(valobj, 'QDateTime'):
        return QDateTimeSynth(valobj)
    elif has_cpp_type(valobj, 'QDir'):
        return QDirSynth(valobj)
    elif has_cpp_type(valobj, 'QEvent'):
        return QEventSynth(valobj)
    elif has_cpp_type(valobj, 'QFile'):
        return QFileSynth(valobj)
    elif has_cpp_type(valobj, 'QFileInfo'):
        return QFileInfoSynth(valobj)
    elif has_cpp_generic_type(valobj, 'QHash'):
        return QHashSynth(valobj)
    elif (has_cpp_generic_type(valobj, 'QHash', '::iterator')
          or has_cpp_generic_type(valobj, 'QHash', '::const_iterator')):
        return QHashIteratorSynth(valobj)
    elif has_cpp_type(valobj, 'QJsonObject'):
        return QJsonObjectSynth(valobj)
    elif has_cpp_type(valobj, 'QJsonValue'):
        return QJsonValueSynth(valobj)
    elif has_cpp_generic_type(valobj, 'QList'):
        return QListSynth(valobj)
    elif has_cpp_type(valobj, 'QLocale'):
        return QLocaleSynth(valobj)
    elif has_cpp_generic_type(valobj, 'QMap'):
        return QMapSynth(valobj)
    elif has_cpp_type(valobj, 'QTemporaryFile'):
        return QTemporaryFileSynth(valobj)
    elif has_cpp_generic_type(valobj, 'QScopedPointer'):
        return QScopedPointerSynth(valobj)
    elif has_cpp_generic_type(valobj, 'QSharedDataPointer'):
        return QSharedDataPointerSynth(valobj)
    elif has_cpp_generic_type(valobj, 'QSharedPointer'):
        return QSharedPointerSynth(valobj)
    elif has_cpp_type(valobj, 'QString'):
        return QStringSynth(valobj)
    elif has_cpp_type(valobj, 'QtCbor::Element'):
        return QtCborElementSynth(valobj)
    elif has_cpp_type(valobj, 'QTemporaryDir'):
        return QTemporaryDirSynth(valobj)
    elif has_cpp_type(valobj, 'QTime'):
        return QTimeSynth(valobj)
    elif has_cpp_type(valobj, 'QTimeZone'):
        return QTimeZoneSynth(valobj)
    elif has_cpp_type(valobj, 'QUrl'):
        return QUrlSynth(valobj)
    elif has_cpp_type(valobj, 'QVariant'):
        return QVariantSynth(valobj)
    elif has_cpp_generic_type(valobj, 'QWeakPointer'):
        return QWeakPointerSynth(valobj)

    return None
