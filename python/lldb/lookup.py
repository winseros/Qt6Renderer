from lldb import SBValue
from qatomicint import qatomicint_summary
from qbitarray import qbitarray_summary, QBitArraySynth
from qbytearray import qbytearray_summary, QByteArraySynth
from qchar import qchar_summary
from qdate import qdate_summary, QDateSynth
from qdatetime import qdatetime_summary, QDateTimeSynth
from pointer import pointer_summary, PointerSynth
from qlist import qlist_summary, QListSynth
from qmap import QMapSynth
from qstring import qstring_summary, QStringSynth
from qtime import qtime_summary, QTimeSynth
from qtimezone import qtimezone_summary, QTimeZoneSynth
from qsharedpointer import qsharedpointer_summary, QSharedPointerSynth
from qshareddatapointer import qshareddatapointer_summary, QSharedDataPointerSynth


def summary_lookup(valobj, dict):
    # type: (SBValue, dict) -> str
    """Returns the summary provider for the given value"""
    type_name = valobj.GetTypeName()
    print('Summary ' + valobj.name + '||' + type_name)
    if type_name.endswith('QString'):
        return qstring_summary(valobj)
    elif type_name.endswith('QString *'):
        return pointer_summary(valobj)
    elif type_name.startswith('QSharedPointer<') and type_name.endswith('>'):
        return qsharedpointer_summary(valobj)
    elif type_name.startswith('QSharedDataPointer<') and type_name.endswith('>'):
        return qshareddatapointer_summary(valobj)
    elif type_name.startswith('QWeakPointer<') and type_name.endswith('>'):
        return qsharedpointer_summary(valobj)
    elif type_name.startswith('QList<') and type_name.endswith('>'):
        return qlist_summary(valobj)
    elif type_name.endswith('QBitArray'):
        return qbitarray_summary(valobj)
    elif type_name.endswith('QByteArray'):
        return qbytearray_summary(valobj)
    elif type_name.endswith('QAtomicInt'):
        return qatomicint_summary(valobj)
    elif type_name.endswith('QChar'):
        return qchar_summary(valobj)
    elif type_name.endswith('QDate'):
        return qdate_summary(valobj)
    elif type_name.endswith('QTime'):
        return qtime_summary(valobj)
    elif type_name.endswith('QDateTime'):
        return qdatetime_summary(valobj)
    elif type_name.endswith('QTimeZone'):
        return qtimezone_summary(valobj)

    return ''


def synthetic_lookup(valobj, dict):
    # type: (SBValue, dict) -> object
    """Returns the synthetic children provider for the given value"""
    type_name = valobj.GetTypeName()
    print('Synth ' + valobj.name + '||' + type_name)
    if type_name.endswith('QString'):
        return QStringSynth(valobj)
    elif type_name.endswith('QString *'):
        return PointerSynth(valobj)
    elif type_name.startswith('QSharedPointer<') and type_name.endswith('>'):
        return QSharedPointerSynth(valobj)
    elif type_name.startswith('QSharedDataPointer<') and type_name.endswith('>'):
        return QSharedDataPointerSynth(valobj)
    elif type_name.startswith('QWeakPointer<') and type_name.endswith('>'):
        return QSharedPointerSynth(valobj)
    elif type_name.startswith('QList<') and type_name.endswith('>'):
        return QListSynth(valobj)
    elif type_name.startswith('QMap<') and type_name.endswith('>'):
        return QMapSynth(valobj)
    elif type_name.endswith('QBitArray'):
        return QBitArraySynth(valobj)
    elif type_name.endswith('QByteArray'):
        return QByteArraySynth(valobj)
    elif type_name.endswith('QDate'):
        return QDateSynth(valobj)
    elif type_name.endswith('QTime'):
        return QTimeSynth(valobj)
    elif type_name.endswith('QDateTime'):
        return QDateTimeSynth(valobj)
    elif type_name.endswith('QTimeZone'):
        return QTimeZoneSynth(valobj)

    return None
