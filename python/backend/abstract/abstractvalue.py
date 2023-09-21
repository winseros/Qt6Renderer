from abc import ABCMeta, abstractmethod
from .abstracttype import AbstractType


class AbstractValue(metaclass=ABCMeta):
    def __init__(self, display_name: str = None):
        self.display_name = display_name

    @abstractmethod
    def get_type(self) -> AbstractType:
        pass

    @abstractmethod
    def get_child(self, name: str) -> 'AbstractValue':
        pass

    @abstractmethod
    def get_pointer_value(self, offset: int = 0, type: AbstractType = None) -> 'AbstractValue':
        pass

    @property
    @abstractmethod
    def native_value(self):
        pass

    @abstractmethod
    def get_display_value(self):
        pass

    @abstractmethod
    def get_python_value(self) -> int:
        pass