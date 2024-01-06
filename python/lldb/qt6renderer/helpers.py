from lldb import SBValue


def has_cpp_type(valobj: SBValue, cpp_name: str) -> bool:
    type_name = _get_type_name(valobj)
    if not type_name:
        return False
    result = type_name == cpp_name
    return result


def has_cpp_generic_type(valobj: SBValue, cpp_name: str, suffix: str = '') -> bool:
    type_name = _get_type_name(valobj)
    if not type_name:
        return False
    result = type_name.startswith(cpp_name + '<') and type_name.endswith(f'>{suffix}')
    return result


def _get_type_name(valobj: SBValue) -> str:
    val_type = valobj.type.GetUnqualifiedType().GetCanonicalType()
    return val_type.name if val_type.IsValid() else None
