from typing import Union, SupportsIndex

class Field:
    bitpos: int
    enumval: int
    name: str
    artificial: bool
    is_base_class: bool
    bitsize: int
    type: 'Type'
    parent_type: 'Type'


class Type:
    alignof: int
    code: str
    dynamic: bool
    name: str
    sizeof: int
    tag: str
    is_scalar: bool
    is_signed: bool

    def fields(self) -> list[Field]: ...

    def array(self, n1: int, n2: int = None) -> 'Type': ...

    def vector(self, n1: int, n2: int = None) -> 'Type': ...

    def const(self) -> 'Type': ...

    def volatile(self) -> 'Type': ...

    def unqualified(self) -> 'Type': ...

    def range(self) -> 'Type': ...

    def reference(self) -> 'Type': ...

    def pointer(self) -> 'Type': ...

    def strip_typedefs(self) -> 'Type': ...

    def target(self) -> 'Type': ...

    def template_argument(self, n: int, block=None) -> 'Type': ...

    def optimized_out(self) -> 'Value': ...


TYPE_CODE_PTR: str
TYPE_CODE_ARRAY: str
TYPE_CODE_STRUCT: str
TYPE_CODE_UNION: str
TYPE_CODE_ENUM: str
TYPE_CODE_FLAGS: str
TYPE_CODE_FUNC: str
TYPE_CODE_INT: str
TYPE_CODE_FLT: str
TYPE_CODE_VOID: str
TYPE_CODE_SET: str
TYPE_CODE_RANGE: str
TYPE_CODE_STRING: str
TYPE_CODE_BITSTRING: str
TYPE_CODE_ERROR: str
TYPE_CODE_METHOD: str
TYPE_CODE_METHODPTR: str
TYPE_CODE_MEMBERPTR: str
TYPE_CODE_REF: str
TYPE_CODE_RVALUE_REF: str
TYPE_CODE_CHAR: str
TYPE_CODE_BOOL: str
TYPE_CODE_COMPLEX: str
TYPE_CODE_TYPEDEF: str
TYPE_CODE_NAMESPACE: str
TYPE_CODE_DECFLOAT: str
TYPE_CODE_INTERNAL_FUNCTION: str
TYPE_CODE_XMETHOD: str
TYPE_CODE_FIXED_POINT: str
TYPE_CODE_NAMESPACE: str


class Value(SupportsIndex):
    address: 'Value'
    is_optimized_out: bool
    type: Type
    dynamic_type: Type
    is_lazy: bool

    def __getitem__(self, key) -> 'Value': ...

    def __add__(self, other) -> 'Value': ...

    def __sub__(self, other) -> 'Value': ...

    def __lshift__(self, other) -> 'Value': ...

    def __rshift__(self, other) -> 'Value': ...

    def __lt__(self, other) -> 'Value': ...

    def __gt__(self, other) -> 'Value': ...

    def __le__(self, other) -> 'Value': ...

    def __ge__(self, other) -> 'Value': ...

    def __rand__(self, other) -> 'Value': ...

    def __index__(self) -> int: ...

    def __int__(self) -> int: ...

    def cast(self, type: Type) -> 'Value': ...

    def dereference(self) -> 'Value': ...

    def referenced_value(self) -> 'Value': ...

    def reference_value(self) -> 'Value': ...

    def const_value(self) -> 'Value': ...

    def dynamic_cast(self, type: Type) -> 'Value': ...

    def reinterpret_cast(self, type: Type) -> 'Value': ...

    def format_string(self) -> str: ...

    def string(self, encoding: str = None, errors: str = None, length: Union[int, 'Value'] = None) -> str: ...

    def lazy_string(self, encoding: str = None, length: Union[int, 'Value'] = None) -> str: ...

    def fetch_lazy(self) -> None: ...


class Symbol:
    type: 'Type'
    line: int
    name: str
    linkage_name: str
    print_name: str
    addr_class: None
    needs_frame: bool
    is_argument: bool
    is_constant: bool
    is_function: bool
    is_variable: bool

    def is_valid(self) -> bool: ...

    def value(self, frame: None) -> 'Value': ...


def lookup_type(type_name: str) -> Type: ...


def parse_and_eval(expr: str) -> Value: ...


def lookup_symbol(name: str, domain: str = None) -> [Symbol, bool]: ...
