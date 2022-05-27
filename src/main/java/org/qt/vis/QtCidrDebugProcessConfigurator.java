package org.qt.vis;

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
import com.jetbrains.cidr.execution.debugger.backend.lldb.LLDBDriver;
import org.jetbrains.annotations.NotNull;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;

public class QtCidrDebugProcessConfigurator implements CidrDebugProcessConfigurator {
    @Override
    public void configure(@NotNull CidrDebugProcess process) {
        IdeaPluginDescriptor plugin = PluginManagerCore.getPlugin(PluginId.getId("org.example.Qt6Renderer"));
        assert plugin != null;
        Path path = plugin.getPluginPath().resolve("python").resolve("lldb");
        String systemPath = FileUtil.toSystemIndependentName(path.toString());
        String escapedPath = StringUtil.escapeStringCharacters(systemPath);

        long threadId = process.getCurrentThreadId();
        int frameIndex = process.getCurrentFrameIndex();

        process.postCommand(debuggerDriver -> {
            if (debuggerDriver instanceof LLDBDriver) {
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, String.format("command script import \"%s/lookup.py\"", escapedPath));
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QString\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QString\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QSharedPointer\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QSharedPointer\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QSharedDataPointer\" --category Qt");
//                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QSharedDataPointer\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QWeakPointer\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QWeakPointer\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QList\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QList\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -x -h \"QMap\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup -x \"QMap\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QBitArray\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QBitArray\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QByteArray\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QByteArray\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QAtomicInt\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QChar\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QDate\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QDate\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QTime\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QTime\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QDateTime\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QDateTime\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type summary add -F lookup.summary_lookup  -e -h \"QTimeZone\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type synthetic add -l lookup.synthetic_lookup \"QTimeZone\" --category Qt");
                debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "type category enable Qt");
            }
        });
    }
}
