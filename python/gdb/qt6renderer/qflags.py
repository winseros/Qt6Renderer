from .baseprinter import StringOnlyPrinter
from gdb.types import make_enum_dict


class QFlagsPrinter(StringOnlyPrinter):
    def to_string(self) -> str:
        val = self._valobj['i']

        enum_type = self._valobj.type.template_argument(0)
        enum_members = make_enum_dict(enum_type)

        text = ''
        for member_name in enum_members:
            member_value = enum_members[member_name]
            if member_value & val:
                if text:
                    text += ' | '
                text = f'{text}{member_name}({member_value})'

        text = f'{val}: {text}' if text else str(val)

        return text
