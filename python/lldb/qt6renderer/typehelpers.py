from lldb import SBType, SBTarget
from typing import List


class TypeHelpers:
    @staticmethod
    def get_template_types(type: SBType, max_types: int, target: SBTarget) -> List[SBType]:
        if type.num_template_args == 0:
            result = TypeHelpers._parse_template_types_from_name(type.name, max_types, target)
            return result

        return type.template_args

    @staticmethod
    def _parse_template_types_from_name(t_name: str, max_types: int, target: SBTarget) -> List[SBType]:
        start_index = t_name.find('<')

        result = []
        if start_index < 0:
            return result

        for i in range(max_types):
            type_name = TypeHelpers._read_type_name(t_name, start_index + 1)
            type_name = TypeHelpers._normalize_type_name(type_name)
            sb_type = target.FindFirstType(type_name)
            result.append(sb_type)
            start_index += len(type_name) + 1

        return result

    @staticmethod
    def _read_type_name(name: str, start_at: int) -> str:
        result = ''
        inner_types = 0
        for i in range(start_at, len(name)):
            char = name[i]
            if inner_types == 0 and (char == ',' or char == '>'):
                return result.strip()
            if char == '<':
                inner_types += 1
            elif char == '>':
                inner_types -= 1
            result += char
        raise 'Incorrect type name'

    @staticmethod
    def _normalize_type_name(type_name: str) -> str:
        # make 'type_name' from, say, 'enum type_name'
        start_index = type_name.find(' ')
        return type_name if start_index < 0 else type_name[start_index + 1:]
