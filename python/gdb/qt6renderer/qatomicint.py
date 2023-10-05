from .baseprinter import StringOnlyPrinter


class QAtomicIntPrinter(StringOnlyPrinter):
    def to_string(self) -> str:
        std_atomic = self._valobj['_q_value']
        std_atomic_val = std_atomic[
            '_M_i']  # The plugin is about Qt, probably we should not dig into the StdLib internals
        return std_atomic_val
