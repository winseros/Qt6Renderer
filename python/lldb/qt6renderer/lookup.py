from lldb import SBValue
from .qt import qt, QtVersion
from .helpers import has_cpp_type, has_cpp_generic_type
from .qatomicint import qatomicint_summary
from .qbitarray import qbitarray_summary, QBitArraySynth


def qt6_lookup_summary(valobj: SBValue, internal_dict):
    if has_cpp_type(valobj, 'QAtomicInt') or has_cpp_type(valobj, 'QBasicAtomicInt'):
        return qatomicint_summary(valobj)
    elif has_cpp_type(valobj, 'QBitArray'):
        return qbitarray_summary(valobj)
    return None


def qt6_lookup_synthetic(valobj: SBValue, internal_dict):
    if has_cpp_type(valobj, 'QBitArray'):
        return QBitArraySynth(valobj)
    return None
