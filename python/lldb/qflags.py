from lldb import SBValue


def qflags_summary(valobj: SBValue) -> str:
    enum_type = valobj.type.GetTemplateArgumentType(0)
    i = valobj.GetChildMemberWithName('i').GetValueAsSigned()

    text = ''
    enum_members = enum_type.GetEnumMembers()
    default = ''
    for m in enum_members:
        if not m.signed:
            default = m.name
        if i & m.signed:
            if len(text):
                text += ' | '
            text += m.name

    return default if not text else text
