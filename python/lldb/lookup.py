from lldb import SBValue
from qatomicint import qatomicint_summary
from qbitarray import qbitarray_summary, QBitArraySynth
from qbytearray import qbytearray_summary, QByteArraySynth
from qchar import qchar_summary
from qdate import qdate_summary, QDateSynth
from qdatetime import qdatetime_summary, QDateTimeSynth
from qdir import qdir_summary, QDirSynth
from qevent import QEventSynth
from qfile import qfile_summary, QFileSynth
from qfileinfo import qfileinfo_summary, QFileInfoSynth
from qflags import qflags_summary
from qhash import qhash_summary, QHashSynth, QHashIteratorSynth
from qhostaddress import qhostaddress_summary
from qlist import qlist_summary, QListSynth
from qlocale import QLocaleSynth
from qmap import QMapSynth
from qstring import qstring_summary, QStringSynth
from qtemporarydir import qtemporarydir_summary, QTemporaryDirSynth
from qtime import qtime_summary, QTimeSynth
from qtimezone import qtimezone_summary, QTimeZoneSynth
from qsharedpointer import qsharedpointer_summary, QSharedPointerSynth
from qshareddatapointer import qshareddatapointer_summary, QSharedDataPointerSynth
from qurl import qurl_summary, QUrlSynth
from quuid import quuid_summary
from qvariant import QVariantSynth


def summary_lookup(valobj: SBValue, dict, opts, replacement_type=None):
    type = valobj.type if replacement_type is None else replacement_type
    type_name = type.name

    if type_name.startswith('const '):
        type_name = type_name[6:]

    print('Summary ' + valobj.name + '||' + type_name)

    if type_name.endswith('QAtomicInt') or type_name.endswith('QBasicAtomicInt'):
        return qatomicint_summary(valobj)
    elif type_name.endswith('QBitArray'):
        return qbitarray_summary(valobj)
    elif type_name.endswith('QByteArray'):
        return qbytearray_summary(valobj)
    elif type_name.endswith('QChar'):
        return qchar_summary(valobj)
    elif type_name.endswith('QDate'):
        return qdate_summary(valobj)
    elif type_name.endswith('QDateTime'):
        return qdatetime_summary(valobj)
    elif type_name.endswith('QDir'):
        return qdir_summary(valobj)
    elif type_name.endswith('QFile'):
        return qfile_summary(valobj)
    elif type_name.endswith('QFileInfo'):
        return qfileinfo_summary(valobj)
    elif type_name.startswith('QFlags<') and type_name.endswith('>'):
        return qflags_summary(valobj)
    elif type_name.startswith('QHash<') and type_name.endswith('>'):
        return qhash_summary(valobj)
    elif type_name.endswith('QHostAddress'):
        return qhostaddress_summary(valobj)
    elif type_name.startswith('QList<') and type_name.endswith('>'):
        return qlist_summary(valobj)
    elif type_name.startswith('QSharedPointer<') and type_name.endswith('>'):
        return qsharedpointer_summary(valobj)
    elif type_name.startswith('QWeakPointer<') and type_name.endswith('>'):
        return qsharedpointer_summary(valobj)
    elif type_name.startswith('QSharedDataPointer<') and type_name.endswith('>'):
        return qshareddatapointer_summary(valobj)
    elif type_name.endswith('QString'):
        return qstring_summary(valobj)
    elif type_name.endswith('QTemporaryDir'):
        return qtemporarydir_summary(valobj)
    elif type_name.endswith('QTime'):
        return qtime_summary(valobj)
    elif type_name.endswith('QTimeZone'):
        return qtimezone_summary(valobj)
    elif type_name.endswith('QUrl'):
        return qurl_summary(valobj)
    elif type_name.endswith('QUuid'):
        return quuid_summary(valobj)

    if type.IsTypedefType():
        type = type.GetTypedefedType()
        return summary_lookup(valobj, dict, opts, type)

    return ''


def synthetic_lookup(valobj: SBValue, dict, replacement_type = None):
    type = valobj.type if replacement_type is None else replacement_type
    type_name = type.name

    if type_name.startswith('const '):
        type_name = type_name[6:]

    print('Synth ' + valobj.name + '||' + type_name)

    if type_name.endswith('QBitArray'):
        return QBitArraySynth(valobj)
    elif type_name.endswith('QByteArray'):
        return QByteArraySynth(valobj)
    elif type_name.endswith('QDate'):
        return QDateSynth(valobj)
    elif type_name.endswith('QDateTime'):
        return QDateTimeSynth(valobj)
    elif type_name.endswith('QDir'):
        return QDirSynth(valobj)
    elif type_name.endswith('QEvent'):
        return QEventSynth(valobj)
    elif type_name.endswith('QFile'):
        return QFileSynth(valobj)
    elif type_name.endswith('QFileInfo'):
        return QFileInfoSynth(valobj)
    elif type_name.startswith('QHash<') and type_name.endswith('>'):
        return QHashSynth(valobj)
    elif type_name.startswith('QHash<') and (
            type_name.endswith('>::iterator') or type_name.endswith('>::const_iterator')):
        return QHashIteratorSynth(valobj)
    elif type_name.startswith('QList<') and type_name.endswith('>'):
        return QListSynth(valobj)
    elif type_name.endswith('QLocale'):
        return QLocaleSynth(valobj)
    elif type_name.startswith('QMap<') and type_name.endswith('>'):
        return QMapSynth(valobj)
    elif type_name.startswith('QSharedDataPointer<') and type_name.endswith('>'):
        return QSharedDataPointerSynth(valobj)
    elif type_name.startswith('QSharedPointer<') and type_name.endswith('>'):
        return QSharedPointerSynth(valobj)
    elif type_name.endswith('QString'):
        return QStringSynth(valobj)
    elif type_name.endswith('QTemporaryDir'):
        return QTemporaryDirSynth(valobj)
    elif type_name.endswith('QTime'):
        return QTimeSynth(valobj)
    elif type_name.endswith('QTimeZone'):
        return QTimeZoneSynth(valobj)
    elif type_name.endswith('QUrl'):
        return QUrlSynth(valobj)
    elif type_name.startswith('QWeakPointer<') and type_name.endswith('>'):
        return QSharedPointerSynth(valobj)
    elif type_name.endswith('QVariant'):
        return QVariantSynth(valobj)

    if type.IsTypedefType():
        type = type.GetTypedefedType()
        return synthetic_lookup(valobj, dict, type)

    return None
