from lldb import SBValue

from .typehelpers import TypeHelpers


def qflags_summary(valobj: SBValue) -> str:
    [enum_type] = TypeHelpers.get_template_types(valobj.type, 1)

    i = valobj.GetChildMemberWithName('i').GetValueAsSigned()

    text = ''
    enum_members = enum_type.enum_members
    default = ''
    for m in enum_members:
        if not m.signed:
            default = m.name
        if i & m.signed:
            if len(text):
                text += ' | '
            text += m.name

    return default if not text else text
