package n.v.k;

import com.intellij.execution.ExecutionException;
import com.intellij.execution.filters.Filter;
import com.intellij.execution.filters.HyperlinkInfo;
import com.intellij.ide.plugins.IdeaPluginDescriptor;
import com.intellij.ide.plugins.PluginManagerCore;
import com.intellij.openapi.extensions.PluginId;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.io.FileUtil;
import com.intellij.openapi.util.text.StringUtil;
import com.jetbrains.cidr.execution.debugger.CidrDebugProcess;
import com.jetbrains.cidr.execution.debugger.CidrDebugProcessConfigurator;
import com.jetbrains.cidr.execution.debugger.backend.DebuggerCommandException;
import com.jetbrains.cidr.execution.debugger.backend.DebuggerDriver;
import com.jetbrains.cidr.execution.debugger.backend.lldb.LLDBDriver;
import com.jetbrains.sourceglider.contextSensitive.input.Bool;
import org.jetbrains.annotations.NotNull;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;

public class QtCidrDebugProcessConfigurator implements CidrDebugProcessConfigurator {
    @Override
    public void configure(@NotNull CidrDebugProcess process) {
        IdeaPluginDescriptor plugin = PluginManagerCore.getPlugin(PluginId.getId("n.v.k.Qt6Renderer"));
        assert plugin != null;
        Path path = plugin.getPluginPath().resolve("python").resolve("lldb");
        String systemPath = FileUtil.toSystemIndependentName(path.toString());
        String escapedPath = StringUtil.escapeStringCharacters(systemPath);

        long threadId = process.getCurrentThreadId();
        int frameIndex = process.getCurrentFrameIndex();

        process.postCommand(debuggerDriver -> {
            if (debuggerDriver instanceof LLDBDriver) {
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, String.format("command script import \"%s/lookup.py\"", escapedPath));

                registerSummary(debuggerDriver, threadId, frameIndex, "QAtomicInt", false);
                registerSummary(debuggerDriver, threadId, frameIndex, "QBasicAtomicInt", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QBitArray", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QByteArray", false);
                registerSummary(debuggerDriver, threadId, frameIndex, "QChar", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QDate", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QDateTime", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QDir", false);
                registerSynth(debuggerDriver, threadId, frameIndex, "QEvent", false);
//                registerBoth(debuggerDriver, threadId, frameIndex, "QFile", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QFileInfo", false);
                registerSummary(debuggerDriver, threadId, frameIndex, "QFlags", true);
                registerBoth(debuggerDriver, threadId, frameIndex, "QHash", true);
                registerSummary(debuggerDriver, threadId, frameIndex, "QHostAddress", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QList", true);
                registerSynth(debuggerDriver, threadId, frameIndex, "QLocale", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QMap", true);
                registerBoth(debuggerDriver, threadId, frameIndex, "QSharedPointer", true);
                registerBoth(debuggerDriver, threadId, frameIndex, "QString", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QTemporaryDir", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QTime", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QTimeZone", false);
                registerBoth(debuggerDriver, threadId, frameIndex, "QWeakPointer", true);
                registerBoth(debuggerDriver, threadId, frameIndex, "QUrl", false);
                registerSummary(debuggerDriver, threadId, frameIndex, "QUuid", false);
                registerSynth(debuggerDriver, threadId, frameIndex, "QVariant", false);

//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup -e -h \"QAtomicInt\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup -e -h \"QBasicAtomicInt\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup -e -h \"QBitArray\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QBitArray\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QByteArray\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QByteArray\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QChar\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QDate\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QDate\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QDateTime\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QDateTime\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QDir\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QDir\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QEvent\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QEvent\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QFile\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QFile\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QFileInfo\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QFileInfo\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QFlags\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QHash\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QHash\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QHostAddress\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QList\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QList\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QLocale\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QMap\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QMap\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QSharedPointer\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QSharedPointer\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QString\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QString\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QTemporaryDir\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QTemporaryDir\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QTime\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QTime\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QTimeZone\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QTimeZone\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QWeakPointer\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QWeakPointer\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QUrl\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QUrl\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QUuid\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QVariant\" --category Qt");

                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type category enable Qt");
            }
        });
    }

    private static void registerBoth(DebuggerDriver driver, long threadId, int frameIndex, String qtType, boolean generic)
            throws DebuggerCommandException, ExecutionException {
        registerSummary(driver, threadId, frameIndex, qtType, generic);
        registerSynth(driver, threadId, frameIndex, qtType, generic);
    }

    private static void registerSummary(DebuggerDriver driver, long threadId, int frameIndex, String qtType, boolean generic)
            throws DebuggerCommandException, ExecutionException {
        String command = "type summary add -F lookup.summary_lookup  -e -h";
        if (generic)
            command += " -x";
        command += " \"" + qtType + "\"";
        command += " --category Qt";
        driver.executeInterpreterCommand(threadId, frameIndex, command);
    }

    private static void registerSynth(DebuggerDriver driver, long threadId, int frameIndex, String qtType, boolean generic)
            throws DebuggerCommandException, ExecutionException {
        String command = "type synthetic add -l lookup.synthetic_lookup";
        if (generic)
            command += " -x";
        command += " \"" + qtType + "\"";
        command += " --category Qt";
        driver.executeInterpreterCommand(threadId, frameIndex, command);
    }
}
