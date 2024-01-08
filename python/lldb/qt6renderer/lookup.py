from lldb import SBValue
from .qt import qt, QtVersion
from .helpers import has_cpp_type, has_cpp_generic_type
from .qatomicint import qatomicint_summary
from .qbitarray import qbitarray_summary, QBitArraySynth
from .qbytearray import qbytearray_summary, QByteArraySynth
from .qchar import qchar_summary
from .qdate import qdate_summary, QDateSynth
from .qdatetime import qdatetime_summary, QDateTimeSynth
from .qdir import qdir_summary, QDirSynth
from .qfile import qfile_summary, QFileSynth, QTemporaryFileSynth
from .qevent import QEventSynth
from .qshareddatapointer import qshareddatapointer_summary, QSharedDataPointerSynth
from .qstring import qstring_summary, QStringSynth


def qt6_lookup_summary(valobj: SBValue, internal_dict):
    qt_version = qt().version()
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
    elif has_cpp_generic_type(valobj, 'QSharedDataPointer'):
        return qshareddatapointer_summary(valobj)
    elif has_cpp_type(valobj, 'QString'):
        return qstring_summary(valobj)

    return None


def qt6_lookup_synthetic(valobj: SBValue, internal_dict):
    qt_version = qt().version()
    if not qt_version or qt_version < QtVersion.V6_0_0:
        return None

    if has_cpp_type(valobj, 'QBitArray'):
        return QBitArraySynth(valobj)
    elif has_cpp_type(valobj, 'QByteArray'):
        return QByteArraySynth(valobj)
    elif has_cpp_type(valobj, 'QDate'):
        return QDateSynth(valobj)
    elif has_cpp_type(valobj, 'QDateTime'):
        return QDateTimeSynth(valobj)
    elif has_cpp_type(valobj, 'QDir'):
        return QDirSynth(valobj)
    elif has_cpp_type(valobj, 'QFile'):
        return QFileSynth(valobj)
    elif has_cpp_type(valobj, 'QTemporaryFile'):
        return QTemporaryFileSynth(valobj)
    elif has_cpp_type(valobj, 'QEvent'):
        return QEventSynth(valobj)
    elif has_cpp_generic_type(valobj, 'QSharedDataPointer'):
        return QSharedDataPointerSynth(valobj)
    elif has_cpp_type(valobj, 'QString'):
        return QStringSynth(valobj)

    return None
