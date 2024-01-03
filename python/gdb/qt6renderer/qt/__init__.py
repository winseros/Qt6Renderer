from gdb import parse_and_eval, lookup_symbol, Value


class Qt:
    def __init__(self):
        self.fallbackQtVersion = 0x60200

    def qtNamespace(self):
        # This function is replaced by handleQtCoreLoaded()
        return ''

    def qtVersionString(self):
        try:
            return str(lookup_symbol('qVersion')[0].value()())
        except:
            pass
        try:
            ns = self.qtNamespace()
            return str(parse_and_eval("((const char*(*)())'%sqVersion')()" % ns))
        except:
            pass
        return None

    def qtVersion(self):
        try:
            # Only available with Qt 5.3+
            qtversion = int(str(parse_and_eval('((void**)&qtHookData)[2]')), 16)
            self.qtVersion = lambda: qtversion
            return qtversion
        except:
            pass

        try:
            version = self.qtVersionString()
            (major, minor, patch) = version[version.find('"') + 1:version.rfind('"')].split('.')
            qtversion = 0x10000 * int(major) + 0x100 * int(minor) + int(patch)
            self.qtVersion = lambda: qtversion
            return qtversion
        except:
            # Use fallback until we have a better answer.
            return self.fallbackQtVersion

    def symbolAddress(self, symbolName) -> Value:
        res = parse_and_eval('(qsizetype*)' + symbolName)
        return None if res is None else res

    def qtHookDataSymbolName(self):
        return 'qtHookData'

    def qtTypeInfoVersion(self):
        addr = self.symbolAddress(self.qtHookDataSymbolName())
        if addr:
            # Only available with Qt 5.3+
            hookVersion = addr.dereference()
            if hookVersion >= 3:
                tiVersion = (addr + 6).dereference()
                self.qtTypeInfoVersion = lambda: tiVersion
                return tiVersion
        return None

