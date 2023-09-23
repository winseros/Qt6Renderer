package n.v.k;

import com.intellij.execution.ExecutionException;
import com.intellij.ide.plugins.IdeaPluginDescriptor;
import com.intellij.openapi.util.io.FileUtil;
import com.intellij.openapi.util.text.StringUtil;
import com.jetbrains.cidr.execution.debugger.CidrDebugProcess;
import com.jetbrains.cidr.execution.debugger.backend.DebuggerCommandException;
import com.jetbrains.cidr.execution.debugger.backend.gdb.GDBDriver;
import org.jetbrains.annotations.NotNull;

import java.nio.file.Path;

public class GDBRegistrar {
    public static void register(@NotNull IdeaPluginDescriptor plugin,
                                @NotNull CidrDebugProcess process, @NotNull GDBDriver debuggerDriver)
            throws DebuggerCommandException, ExecutionException {

        Path path = plugin.getPluginPath().resolve("python").resolve("gdb");
        String systemPath = FileUtil.toSystemIndependentName(path.toString());
        String escapedPath = StringUtil.escapeStringCharacters(systemPath);

        long threadId = process.getCurrentThreadId();
        int frameIndex = process.getCurrentFrameIndex();

        debuggerDriver.executeInterpreterCommand(threadId, frameIndex, String.format("python sys.path.append(\"%s\")", escapedPath));
        debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "python import qt6renderer");
        debuggerDriver.executeInterpreterCommand(threadId, frameIndex, "python gdb.pretty_printers.append(qt6renderer.qt6_lookup)");
    }
}
