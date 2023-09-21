from abc import ABCMeta, abstractmethod


class AbstractType(metaclass=ABCMeta):
    @abstractmethod
    def get_pointer_type(self) -> 'AbstractType':
        pass

    @abstractmethod
    def get_reference_type(self) -> 'AbstractType':
        pass

    @abstractmethod
    def get_target_type(self) -> 'AbstractType':
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    @property
    @abstractmethod
    def native_type(self):
        pass
