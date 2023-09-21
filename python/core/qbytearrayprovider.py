from .abstractprovider import AbstractSummaryProvider


class QByteArraySummaryProvider(AbstractSummaryProvider):
    def to_string(self) -> str:
        d = self._value.get_child('d')
        d_size = d.get_child('size')

        return f'size={d_size.native_value.to_string()}'
