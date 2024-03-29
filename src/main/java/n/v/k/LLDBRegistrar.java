package n.v.k;

import com.intellij.execution.ExecutionException;
import com.intellij.ide.plugins.IdeaPluginDescriptor;
import com.intellij.openapi.util.io.FileUtil;
import com.intellij.openapi.util.text.StringUtil;
import com.jetbrains.cidr.execution.debugger.CidrDebugProcess;
import com.jetbrains.cidr.execution.debugger.backend.DebuggerCommandException;
import com.jetbrains.cidr.execution.debugger.backend.DebuggerDriver;
import com.jetbrains.cidr.execution.debugger.backend.lldb.LLDBDriver;
import org.jetbrains.annotations.NotNull;

import java.nio.file.Path;

class LLDBRegistrar {
    public static void register(@NotNull IdeaPluginDescriptor plugin,
                                @NotNull CidrDebugProcess process, @NotNull LLDBDriver debuggerDriver)
            throws DebuggerCommandException, ExecutionException {

        Path path = plugin.getPluginPath().resolve("python").resolve("lldb");
        String systemPath = FileUtil.toSystemIndependentName(path.toString());
        String escapedPath = StringUtil.escapeStringCharacters(systemPath);

        long threadId = process.getCurrentThreadId();
        int frameIndex = process.getCurrentFrameIndex();

        debuggerDriver.executeInterpreterCommand(threadId, frameIndex, String.format("command script import \"%s/qt6renderer\"", escapedPath));

        registerSummary(debuggerDriver, threadId, frameIndex, "QAtomicInt", false);
        registerSummary(debuggerDriver, threadId, frameIndex, "QBasicAtomicInt", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QBitArray", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QByteArray", false);
        registerSummary(debuggerDriver, threadId, frameIndex, "QChar", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QDate", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QDateTime", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QDir", false);
        registerSynth(debuggerDriver, threadId, frameIndex, "QEvent", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QFile", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QFileInfo", false);
        registerSummary(debuggerDriver, threadId, frameIndex, "QFlags", true);
        registerBoth(debuggerDriver, threadId, frameIndex, "QHash", true);
        registerSummary(debuggerDriver, threadId, frameIndex, "QHostAddress", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QList", true);
        registerSynth(debuggerDriver, threadId, frameIndex, "QLocale", false);
        registerSynth(debuggerDriver, threadId, frameIndex, "QMap", true);
        registerBoth(debuggerDriver, threadId, frameIndex, "QScopedPointer", true);
        registerBoth(debuggerDriver, threadId, frameIndex, "QSharedPointer", true);
        registerBoth(debuggerDriver, threadId, frameIndex, "QSharedDataPointer", true);
        registerBoth(debuggerDriver, threadId, frameIndex, "QString", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QTemporaryFile", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QTemporaryDir", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QTime", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QTimeZone", false);
        registerBoth(debuggerDriver, threadId, frameIndex, "QWeakPointer", true);
        registerBoth(debuggerDriver, threadId, frameIndex, "QUrl", false);
        registerSummary(debuggerDriver, threadId, frameIndex, "QUuid", false);
        registerSynth(debuggerDriver, threadId, frameIndex, "QVariant", false);

        debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type category enable Qt");
    }

    private static void registerBoth(DebuggerDriver driver, long threadId, int frameIndex, String qtType, boolean generic)
            throws DebuggerCommandException, ExecutionException {
        registerSummary(driver, threadId, frameIndex, qtType, generic);
        registerSynth(driver, threadId, frameIndex, qtType, generic);
    }

    private static void registerSummary(DebuggerDriver driver, long threadId, int frameIndex, String qtType, boolean generic)
            throws DebuggerCommandException, ExecutionException {
        String command = "type summary add -F qt6renderer.qt6_lookup_summary  -e -h";
        if (generic)
            command += " -x";
        command += " \"" + qtType + "\"";
        command += " --category Qt";
        driver.executeInterpreterCommand(threadId, frameIndex, command);
    }

    private static void registerSynth(DebuggerDriver driver, long threadId, int frameIndex, String qtType, boolean generic)
            throws DebuggerCommandException, ExecutionException {
        String command = "type synthetic add -l qt6renderer.qt6_lookup_synthetic";
        if (generic)
            command += " -x";
        command += " \"" + qtType + "\"";
        command += " --category Qt";
        driver.executeInterpreterCommand(threadId, frameIndex, command);
    }
}
