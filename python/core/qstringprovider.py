from .abstractprovider import AbstractSummaryProvider


class QStringSummaryProvider(AbstractSummaryProvider):
    def to_string(self) -> str:
        return 'QString_Summary'
