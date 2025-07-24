import sys
import os

# This is derived from the code in:
# https://github.com/winseros/Qt6RendererIntlj/blob/develop/src/main/java/n/v/k/LLDBRegistrar.java

def __lldb_init_module(debugger, unused):
    parent = os.path.dirname(os.path.abspath(__file__))
    debugger.HandleCommand('command script import ' + os.path.join(parent, 'qt6renderer'))
    registerSummary(debugger, 'QAtomicInt', False);
    registerSummary(debugger, 'QBasicAtomicInt', False);
    registerBoth(debugger, 'QBitArray', False);
    registerBoth(debugger, 'QByteArray', False);
    registerSummary(debugger, 'QChar', False);
    registerBoth(debugger, 'QDate', False);
    registerBoth(debugger, 'QDateTime', False);
    registerBoth(debugger, 'QDir', False);
    registerSynth(debugger, 'QEvent', False);
    registerBoth(debugger, 'QFile', False);
    registerBoth(debugger, 'QFileInfo', False);
    registerSummary(debugger, '^QFlags<.*', True);
    registerBoth(debugger, '^QHash<.*', True);
    registerSummary(debugger, 'QHostAddress', False);
    registerBoth(debugger, '^QList<.*', True);
    registerSynth(debugger, 'QLocale', False);
    registerSynth(debugger, '^QMap<.*', True);
    registerBoth(debugger, '^QScopedPointer<.*', True);
    registerBoth(debugger, '^QSharedPointer<.*', True);
    registerBoth(debugger, '^QSharedDataPointer<.*', True);
    registerBoth(debugger, 'QString', False);
    registerBoth(debugger, 'QTemporaryFile', False);
    registerBoth(debugger, 'QTemporaryDir', False);
    registerBoth(debugger, 'QTime', False);
    registerBoth(debugger, 'QTimeZone', False);
    registerBoth(debugger, '^QWeakPointer<.*', True);
    registerBoth(debugger, 'QUrl', False);
    registerSummary(debugger, 'QUuid', False);
    registerSynth(debugger, 'QVariant', False);
    debugger.HandleCommand('type category enable Qt')


def registerBoth(debugger, qtType, generic):
    registerSummary(debugger, qtType, generic)
    registerSynth(debugger, qtType, generic)

def registerSummary(debugger, qtType, generic):
    command = 'type summary add -F qt6renderer.qt6_lookup_summary  -e -h'
    if generic:
        command += ' -x'
    command += ' "' + qtType + '"'
    command += ' --category Qt'
    debugger.HandleCommand(command)

def registerSynth(debugger, qtType, generic):
    command = 'type synthetic add -l qt6renderer.qt6_lookup_synthetic'
    if generic:
        command += ' -x'
    command += ' \"' + qtType + '\"'
    command += ' --category Qt'
    debugger.HandleCommand(command)
