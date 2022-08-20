from lldb import SBValue
from helpers import TypeHelpers


def qflags_summary(valobj: SBValue) -> str:
    if valobj.type.GetNumberOfTemplateArguments() > 0:
        enum_type = valobj.type.GetTemplateArgumentType(0)
    else:
        module = valobj.GetFrame().GetModule()
        [enum_type] = TypeHelpers.read_template_types(module, valobj.type, 1)

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
